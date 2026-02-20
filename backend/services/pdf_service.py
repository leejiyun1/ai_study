# [Service] PDF 텍스트 추출 로직
import PyPDF2
from io import BytesIO
from typing import List

# [function] PDF 파일에서 텍스트 추출 후 반환
async def extract_text(file) -> str:
    # [validation] 파일 기본 검증
    if not file or not file.filename:
        raise ValueError("INVALID_FILE")
    if not file.filename.lower().endswith(".pdf"):
        raise ValueError("INVALID_FILE")

    # [read] 업로드 파일 바이트 읽기
    file_bytes = await file.read()
    if not file_bytes:
        raise ValueError("INVALID_FILE")

    # [parse] 페이지별 텍스트 추출
    try:
        reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        pages_text = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            pages_text.append(page_text)
    except Exception as exc:
        raise ValueError("PDF_PARSE_FAILED") from exc

    # [normalize] 공백 정리 후 반환
    joined_text = "\n".join(pages_text)
    normalized = " ".join(joined_text.split())
    if not normalized:
        raise ValueError("PDF_PARSE_FAILED")
    return normalized


# [function] 원문을 청크 단위로 분할
def split_text_into_chunks(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200,
) -> List[str]:
    # [validation] 파라미터 검증
    if not text or not text.strip():
        return []
    if chunk_size <= 0:
        raise ValueError("INVALID_CHUNK_SIZE")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("INVALID_CHUNK_OVERLAP")

    # [chunking] 겹침(overlap) 포함 슬라이딩 윈도우 분할
    chunks = []
    start = 0
    step = chunk_size - overlap
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += step

    return chunks
