# [Service] PDF 텍스트 추출 로직
import os
import PyPDF2
from io import BytesIO
from typing import List

try:
    import pytesseract
    from pdf2image import convert_from_bytes
except ImportError:
    pytesseract = None
    convert_from_bytes = None

# [env] OCR 설정
OCR_ENABLED = os.getenv("OCR_ENABLED", "true").lower() == "true"
OCR_LANG = os.getenv("OCR_LANG", "kor+eng")
OCR_DPI = int(os.getenv("OCR_DPI", "200"))
OCR_MIN_TEXT_LENGTH = int(os.getenv("OCR_MIN_TEXT_LENGTH", "300"))


# [function] 공백 정규화
def _normalize_text(text: str) -> str:
    return " ".join((text or "").split())


# [function] OCR 기반 텍스트 추출
def _extract_text_with_ocr(file_bytes: bytes) -> str:
    if not OCR_ENABLED:
        return ""
    if pytesseract is None or convert_from_bytes is None:
        return ""

    images = convert_from_bytes(file_bytes, dpi=OCR_DPI)
    ocr_texts = []
    for image in images:
        text = pytesseract.image_to_string(image, lang=OCR_LANG)
        ocr_texts.append(text)
    return _normalize_text("\n".join(ocr_texts))


# [function] PDF 파일에서 텍스트 추출 후 반환
async def extract_text(file, max_file_size_bytes: int | None = None) -> str:
    # [validation] 파일 기본 검증
    if not file or not file.filename:
        raise ValueError("INVALID_FILE")
    if not file.filename.lower().endswith(".pdf"):
        raise ValueError("INVALID_FILE")

    # [read] 업로드 파일 바이트 읽기
    file_bytes = await file.read()
    if not file_bytes:
        raise ValueError("INVALID_FILE")
    if max_file_size_bytes is not None and len(file_bytes) > max_file_size_bytes:
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

    # [normalize] 1차(PyPDF2) 텍스트 정리
    joined_text = "\n".join(pages_text)
    normalized = _normalize_text(joined_text)

    # [fallback] 텍스트가 부족하면 OCR 보조 추출
    if len(normalized) < OCR_MIN_TEXT_LENGTH:
        ocr_text = _extract_text_with_ocr(file_bytes)
        if len(ocr_text) > len(normalized):
            normalized = ocr_text

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
