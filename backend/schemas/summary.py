# [Schema] 요청/응답 데이터 형식 정의 - Pydantic 모델
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# [class] 배치 처리 결과 아이템
class BatchItemResponse(BaseModel):
    document_id: int
    filename: str
    status: str
    message: str


# [class] 배치 처리 응답
class BatchResponse(BaseModel):
    batch_total: int
    results: List[BatchItemResponse]


# [class] 요약 목록 아이템
class SummaryListItemResponse(BaseModel):
    id: int
    title: Optional[str] = None
    filename: str
    status: str
    created_at: datetime

    # [config] ORM 모델과 연동 설정
    class Config:
        orm_mode = True


# [class] 요약 상세 응답
class SummaryResponse(BaseModel):
    id: int
    title: Optional[str] = None
    filename: str
    summary: Optional[str] = None
    status: str
    error_message: Optional[str] = None
    created_at: datetime

    # [config] ORM 모델과 연동 설정
    class Config:
        orm_mode = True
