# [Router] 엔드포인트 정의 및 서비스 호출
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import pdf_service, llm_service

# [instance] 라우터 인스턴스 생성
router = APIRouter()

# [POST] PDF 업로드 및 요약 요청
@router.post("/summarize")
async def summarize(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # pdf_service로 텍스트 추출
    # llm_service로 요약 요청
    # DB 저장
    # 결과 반환
    pass

# [GET] 요약 목록 조회
@router.get("/summaries")
async def get_summaries(db: Session = Depends(get_db)):
    # DB에서 목록 조회 후 반환
    pass

# [GET] 요약 상세 조회
@router.get("/summaries/{id}")
async def get_summary(id: int, db: Session = Depends(get_db)):
    # DB에서 id로 조회 후 반환
    pass

# [GET] 요약본 TXT 다운로드
@router.get("/summaries/{id}/download")
async def download_summary(id: int, db: Session = Depends(get_db)):
    # DB에서 요약본 가져와서 TXT로 반환
    pass