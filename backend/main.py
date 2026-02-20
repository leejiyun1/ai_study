# [FastAPI] 앱 진입점 - 서버 시작 시 가장 먼저 실행되는 파일
from fastapi import FastAPI
from routers import summarize

# [instance] FastAPI 앱 인스턴스 생성
app = FastAPI()

# [router] summarize 라우터 등록 - /summarize 관련 엔드포인트 연결
app.include_router(summarize.router)