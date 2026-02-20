# [Model] DB 테이블과 매핑되는 클래스 - 테이블 구조 정의
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

# [class] Summary 테이블 정의 - 요약 결과를 저장하는 테이블
class Summary(Base):
    # 테이블명 정의
    # 각 컬럼들 정의
    pass