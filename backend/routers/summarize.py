# [Router] 엔드포인트 정의 및 서비스 호출
import json
import logging
import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from database import get_db
from models.summary import Summary, DocumentChunk
from schemas.summary import BatchResponse, SummaryListItemResponse, SummaryResponse
from services import pdf_service, llm_service
from services.llm_service import GeminiServiceError

# [instance] 라우터 인스턴스 생성
router = APIRouter()
logger = logging.getLogger(__name__)

# [const] 외부 노출 허용 에러 코드
ALLOWED_ERROR_CODES = {
    "INVALID_FILE",
    "PDF_PARSE_FAILED",
    "GEMINI_FAILED",
    "DB_ERROR",
}

# [const] 배치/파일/청킹 설정값
MAX_UPLOAD_FILES = int(os.getenv("MAX_UPLOAD_FILES", "10"))
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "20"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))


# [function] 예외를 표준 에러 코드로 정규화
def normalize_error_code(exc: Exception) -> str:
    code = str(exc).strip()
    if code in ALLOWED_ERROR_CODES:
        return code
    return "DB_ERROR"


# [POST] PDF 다중 업로드 및 순차 요약 요청
@router.post("/summarize/batch", response_model=BatchResponse)
async def summarize_batch(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    if not files:
        raise HTTPException(status_code=400, detail="INVALID_FILE")
    if len(files) > MAX_UPLOAD_FILES:
        raise HTTPException(status_code=400, detail="INVALID_FILE")

    results = []
    for file in files:
        try:
            # [pipeline] 텍스트 추출 -> 청킹 -> 임베딩 -> 요약
            text = await pdf_service.extract_text(
                file,
                max_file_size_bytes=MAX_FILE_SIZE_MB * 1024 * 1024,
            )
            chunks = pdf_service.split_text_into_chunks(
                text,
                chunk_size=CHUNK_SIZE,
                overlap=CHUNK_OVERLAP,
            )
            vectors = await llm_service.embed_chunks(chunks)
            summary_result = await llm_service.summarize(text)

            # [save] 성공 시에만 문서 레코드 저장
            document = Summary(
                original_filename=file.filename or "",
                original_text=text,
                summary_title=summary_result["title"],
                summary_text=summary_result["summary"],
                status="COMPLETED",
                error_message=None,
            )
            db.add(document)
            db.flush()

            # [save] 청크/임베딩 저장
            for idx, (chunk_text, embedding) in enumerate(zip(chunks, vectors)):
                db.add(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_index=idx,
                        chunk_text=chunk_text,
                        embedding_json=json.dumps(embedding),
                    )
                )

            db.commit()
            db.refresh(document)
            results.append(
                {
                    "document_id": document.id,
                    "filename": file.filename or "",
                    "status": "COMPLETED",
                    "message": "processed",
                }
            )
        except Exception as exc:
            error_code = normalize_error_code(exc)
            if isinstance(exc, GeminiServiceError):
                logger.warning(
                    "Gemini failed for filename=%s detail=%s",
                    file.filename or "",
                    exc.detail,
                )
            else:
                logger.exception(
                    "Pipeline failed for filename=%s",
                    file.filename or "",
                )
            db.rollback()
            results.append(
                {
                    "document_id": 0,
                    "filename": file.filename or "",
                    "status": "FAILED",
                    "message": error_code,
                }
            )

    return {"batch_total": len(files), "results": results}

# [GET] 요약 목록 조회
@router.get("/summaries", response_model=list[SummaryListItemResponse])
async def get_summaries(db: Session = Depends(get_db)):
    summaries = db.query(Summary).order_by(Summary.created_at.desc()).all()
    return [
        {
            "id": item.id,
            "title": item.summary_title,
            "filename": item.original_filename,
            "status": item.status,
            "created_at": item.created_at,
        }
        for item in summaries
    ]

# [GET] 요약 상세 조회
@router.get("/summaries/{id}", response_model=SummaryResponse)
async def get_summary(id: int, db: Session = Depends(get_db)):
    item = db.query(Summary).filter(Summary.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="NOT_FOUND")

    return {
        "id": item.id,
        "title": item.summary_title,
        "filename": item.original_filename,
        "summary": item.summary_text,
        "status": item.status,
        "error_message": item.error_message,
        "created_at": item.created_at,
    }

# [GET] 요약본 TXT 다운로드
@router.get("/summaries/{id}/download")
async def download_summary(id: int, db: Session = Depends(get_db)):
    item = db.query(Summary).filter(Summary.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    if not item.summary_text:
        raise HTTPException(status_code=400, detail="NOT_READY")

    filename = f"summary_{id}.txt"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    content = f"제목: {item.summary_title or ''}\n\n요약:\n{item.summary_text}"
    return PlainTextResponse(content=content, headers=headers)
