# [Schema] 요청/응답 데이터 형식 정의 - Pydantic 모델
from pydantic import BaseModel
from datetime import datetime

# [class] 요약 요청 스키마
class SummaryResponse(BaseModel):
    # 각 필드 정의

    # [config] ORM 모델과 연동 설정
    class Config:
        pass