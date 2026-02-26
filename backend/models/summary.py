# [Model] DB 테이블과 매핑되는 클래스 - 테이블 구조 정의
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

# [class] Summary 테이블 정의 - 요약 결과를 저장하는 테이블
class Summary(Base):
    # [table] 테이블명
    __tablename__ = "documents"

    # [PK] 문서 고유 ID
    id = Column(Integer, primary_key=True, index=True)
    # [Field] 업로드된 원본 파일명
    original_filename = Column(String(255), nullable=False)
    # [Field] 원본 전체 텍스트
    original_text = Column(Text, nullable=False)
    # [Field] AI가 생성한 제목
    summary_title = Column(String(255), nullable=True)
    # [Field] AI가 생성한 요약문
    summary_text = Column(Text, nullable=True)
    # [Field] 처리 상태 (PENDING | COMPLETED | FAILED)
    status = Column(String(20), nullable=False, default="PENDING")
    # [Field] 실패 시 에러 메시지
    error_message = Column(Text, nullable=True)
    # [Field] 생성 시각
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # [Field] 수정 시각
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


# [class] DocumentChunk 테이블 정의 - 원문 청크와 임베딩 저장
class DocumentChunk(Base):
    # [table] 테이블명
    __tablename__ = "document_chunks"

    # [PK] 청크 고유 ID
    id = Column(Integer, primary_key=True, index=True)
    # [Field] 상위 문서 ID
    document_id = Column(Integer, nullable=False, index=True)
    # [Field] 문서 내 청크 순번
    chunk_index = Column(Integer, nullable=False)
    # [Field] 청크 텍스트
    chunk_text = Column(Text, nullable=False)
    # [Field] 임베딩 JSON 문자열
    embedding_json = Column(Text, nullable=False)
    # [Field] 생성 시각
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
