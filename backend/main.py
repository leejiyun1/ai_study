# [FastAPI] 앱 진입점 - 서버 시작 시 가장 먼저 실행되는 파일
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from models import summary as summary_models  # noqa: F401
from routers import summarize

# [instance] FastAPI 앱 인스턴스 생성
app = FastAPI()

# [middleware] CORS 허용 설정 (개발 환경)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [startup] 서버 시작 시 테이블 자동 생성
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# [router] summarize 라우터 등록 - /summarize 관련 엔드포인트 연결
app.include_router(summarize.router, prefix="/api")
