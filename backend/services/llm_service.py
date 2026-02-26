# [Service] Gemini API 호출 및 요약/임베딩 로직
import asyncio
import json
import os
from urllib.error import HTTPError, URLError
from urllib import parse, request
from prompts.summarize_prompt import SUMMARIZE_PROMPT

# [env] Gemini 설정
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_SUMMARY = os.getenv("GEMINI_MODEL_SUMMARY", "gemini-2.0-flash")
GEMINI_MODEL_EMBEDDING = os.getenv("GEMINI_MODEL_EMBEDDING", "text-embedding-004")
SUMMARY_MAX_CHARS = int(os.getenv("SUMMARY_MAX_CHARS", "40000"))


# [class] Gemini 서비스 예외
class GeminiServiceError(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(code)
        self.code = code
        self.detail = detail


# [function] Gemini REST API 요청
def _post_gemini(path: str, payload: dict) -> dict:
    if not GEMINI_API_KEY:
        raise GeminiServiceError("GEMINI_FAILED", "GEMINI_API_KEY is missing")

    url = f"https://generativelanguage.googleapis.com/v1beta/{path}?{parse.urlencode({'key': GEMINI_API_KEY})}"
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url=url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        raise GeminiServiceError("GEMINI_FAILED", f"HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise GeminiServiceError("GEMINI_FAILED", f"URL_ERROR: {exc.reason}") from exc
    except Exception as exc:
        raise GeminiServiceError("GEMINI_FAILED", f"UNEXPECTED: {exc}") from exc


# [function] Gemini 응답 텍스트 추출
def _extract_text_from_generate_content(resp: dict) -> str:
    try:
        return resp["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as exc:
        raise GeminiServiceError("GEMINI_FAILED", f"INVALID_GENERATE_RESPONSE: {resp}") from exc


# [function] 모델 응답의 코드 블록 제거
def _strip_json_fence(raw_text: str) -> str:
    cleaned = (raw_text or "").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
    return cleaned


# [function] 텍스트를 받아 AI 요약 결과 반환
async def summarize(text: str) -> dict:
    if not text or not text.strip():
        raise GeminiServiceError("GEMINI_FAILED", "EMPTY_SUMMARY_INPUT")

    truncated_text = text[:SUMMARY_MAX_CHARS]
    prompt_text = SUMMARIZE_PROMPT.format(text=truncated_text)
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {"temperature": 0.2},
    }

    response = await asyncio.to_thread(
        _post_gemini,
        f"models/{GEMINI_MODEL_SUMMARY}:generateContent",
        payload,
    )
    raw = _extract_text_from_generate_content(response)
    cleaned_raw = _strip_json_fence(raw)

    try:
        parsed = json.loads(cleaned_raw)
        title = (parsed.get("title") or "").strip()
        summary = (parsed.get("summary") or "").strip()
    except Exception as exc:
        raise GeminiServiceError(
            "GEMINI_FAILED",
            f"SUMMARY_JSON_PARSE_FAILED raw={raw} cleaned={cleaned_raw}",
        ) from exc

    if not title or not summary:
        raise GeminiServiceError(
            "GEMINI_FAILED",
            f"SUMMARY_FIELDS_EMPTY raw={raw} cleaned={cleaned_raw}",
        )

    return {"title": title, "summary": summary}


# [function] 단일 텍스트 임베딩 생성
async def embed_text(text: str) -> list[float]:
    if not text or not text.strip():
        raise GeminiServiceError("GEMINI_FAILED", "EMPTY_EMBED_INPUT")

    payload = {"content": {"parts": [{"text": text}]}}
    response = await asyncio.to_thread(
        _post_gemini,
        f"models/{GEMINI_MODEL_EMBEDDING}:embedContent",
        payload,
    )

    try:
        values = response["embedding"]["values"]
    except Exception as exc:
        raise GeminiServiceError("GEMINI_FAILED", f"INVALID_EMBED_RESPONSE: {response}") from exc

    if not isinstance(values, list) or len(values) == 0:
        raise GeminiServiceError("GEMINI_FAILED", f"EMPTY_EMBED_VALUES: {response}")
    return values


# [function] 청크 리스트 임베딩 생성
async def embed_chunks(chunks: list[str]) -> list[list[float]]:
    vectors = []
    for chunk in chunks:
        vector = await embed_text(chunk)
        vectors.append(vector)
    return vectors
