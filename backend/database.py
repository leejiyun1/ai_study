# [database] DB 연결 설정 파일
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# [dotenv] .env 파일에서 환경변수 로드
load_dotenv()

# [env] .env 파일에서 DB URL 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

# [engine] DB 연결 엔진 생성
engine = create_engine(DATABASE_URL)

# [session] DB 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# [Base] 모든 모델 클래스가 상속받는 베이스 클래스
Base = declarative_base()

# [dependency] 라우터에서 DB 세션을 주입받기 위한 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()