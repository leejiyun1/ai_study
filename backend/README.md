# PDF 문서 요약 시스템 - 개발 가이드

## 1. 프로젝트 개요

사용자가 PDF 파일을 업로드하면 텍스트를 추출하고, OpenAI API를 호출하여 요약한 결과를 반환하는 웹 애플리케이션입니다.

- **프론트엔드**: React (Vite) + TailwindCSS + Axios
- **백엔드**: FastAPI + SQLAlchemy + MariaDB
- **AI**: OpenAI GPT-4o mini API
- **PDF 파싱**: PyPDF2

---

## 2. 전체 흐름

```
[React] PDF 업로드
    ↓
[FastAPI] 파일 수신
    ↓
[pdf_service] 텍스트 추출
    ↓
[llm_service] OpenAI API 호출 (요약)
    ↓
[DB] 요약 결과 저장
    ↓
[React] 요약 결과 표시
```

---

## 3. 환경 세팅

### 3-0. 사전 준비

아래 항목이 미리 설치되어 있어야 합니다.

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [MariaDB](https://mariadb.org/download/)
- [Git](https://git-scm.com/)

### 3-1. 프로젝트 클론 및 가상환경 생성

```bash
git clone 레포주소
cd mini-project

conda create -n mini-project python=3.11
conda activate mini-project
```

### 3-2. 라이브러리 설치

```bash
cd backend
pip install -r requirements.txt
```

### 3-3. 환경변수 설정

`.env.example` 파일을 복사해서 `.env` 파일을 생성합니다.

```bash
cp .env.example .env
```

이후 `.env` 파일을 열어 DB 비밀번호와 OpenAI API 키를 입력합니다.

## 4. 폴더 구조

```
backend/
├── routers/
│   └── summarize.py        # 엔드포인트 정의
├── services/
│   ├── pdf_service.py      # PDF 텍스트 추출 로직
│   └── llm_service.py      # OpenAI API 호출 로직
├── models/
│   └── summary.py          # DB 테이블 정의
├── schemas/
│   └── summary.py          # 요청/응답 데이터 형식 정의
├── prompts/
│   └── summarize_prompt.py # AI에게 보낼 프롬프트 템플릿
├── database.py             # DB 연결 설정
├── main.py                 # 앱 진입점
└── requirements.txt        # 라이브러리 목록
```

---

## 5. 주석 스타일 가이드

이 프로젝트에서는 코드의 각 요소가 무엇인지 바로 알 수 있도록 아래 형식의 주석을 사용합니다.

```python
# [태그] 설명
```

| 태그         | 의미                  |
| ------------ | --------------------- |
| `[class]`    | 클래스 정의           |
| `[function]` | 함수 정의             |
| `[instance]` | 인스턴스 생성         |
| `[Model]`    | DB 테이블 매핑 클래스 |
| `[Schema]`   | 요청/응답 데이터 형식 |
| `[Router]`   | 엔드포인트 정의       |
| `[Service]`  | 비즈니스 로직         |
| `[env]`      | 환경변수              |
| `[Field]`    | DB 컬럼               |
| `[PK]`       | Primary Key           |

---

## 6. 각 파일 설명 및 예시

### 6-1. main.py

앱이 시작될 때 가장 먼저 실행되는 파일입니다. FastAPI 인스턴스를 생성하고 라우터를 등록합니다.

```python
# [FastAPI] 앱 진입점 - 서버 시작 시 가장 먼저 실행되는 파일
from fastapi import FastAPI
from routers import summarize

# [instance] FastAPI 앱 인스턴스 생성
app = FastAPI()

# [router] summarize 라우터 등록 - /summarize 관련 엔드포인트 연결
app.include_router(summarize.router)
```

---

### 6-2. database.py

DB 연결 설정을 담당하는 파일입니다. 라우터에서 DB 세션을 주입받아 사용합니다.

```python
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
```

---

### 6-3. models/summary.py

DB 테이블 구조를 정의하는 파일입니다. 클래스 하나가 테이블 하나와 1:1 매핑됩니다.

**[작성 가이드]**

```python
# [Model] DB 테이블과 매핑되는 클래스 - 테이블 구조 정의
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

# [class] Summary 테이블 정의 - 요약 결과를 저장하는 테이블
class Summary(Base):
    # 테이블명 정의
    # 각 컬럼들 정의
    pass
```

**컬럼 구성 참고**

| 컬럼명            | 타입         | 설명                  |
| ----------------- | ------------ | --------------------- |
| id                | Integer (PK) | 고유 식별자           |
| title             | String(255)  | AI가 추출한 문서 제목 |
| original_filename | String(255)  | 업로드된 PDF 파일명   |
| summary           | Text         | 요약 본문             |
| created_at        | DateTime     | 생성 일시             |

---

### 6-4. schemas/summary.py

API 요청/응답 데이터 형식을 정의하는 파일입니다. Pydantic을 사용합니다.

**[작성 가이드]**

```python
# [Schema] 요청/응답 데이터 형식 정의 - Pydantic 모델
from pydantic import BaseModel
from datetime import datetime

# [class] 요약 응답 스키마
class SummaryResponse(BaseModel):
    # 각 필드 정의

    # [config] ORM 모델과 연동 설정
    class Config:
        pass
```

---

### 6-5. prompts/summarize_prompt.py

OpenAI API에 전달할 프롬프트 템플릿을 정의하는 파일입니다.

**[작성 가이드]**

```python
# [Prompt] LLM에게 전달할 프롬프트 템플릿 정의

# [str] 요약 요청 프롬프트 - 제목과 요약본을 함께 추출
SUMMARIZE_PROMPT = """
# 프롬프트 내용 작성
"""
```

**프롬프트 작성 시 포함할 내용**

- 문서 제목 추출 요청
- 핵심 내용 요약 요청
- 응답 형식 지정 (제목 / 요약 구분)

---

### 6-6. services/pdf_service.py

PDF 파일에서 텍스트를 추출하는 로직을 담당합니다.

**[작성 가이드]**

```python
# [Service] PDF 텍스트 추출 로직
import PyPDF2

# [function] PDF 파일에서 텍스트 추출 후 반환
async def extract_text(file) -> str:
    # 파일 읽기
    # 텍스트 추출 및 반환
    pass
```

---

### 6-7. services/llm_service.py

OpenAI API를 호출하여 텍스트를 요약하는 로직을 담당합니다.

**[작성 가이드]**

```python
# [Service] OpenAI API 호출 및 요약 로직
from openai import AsyncOpenAI
from prompts.summarize_prompt import SUMMARIZE_PROMPT
import os

# [instance] OpenAI 클라이언트 생성
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# [function] 텍스트를 받아 AI 요약 결과 반환
async def summarize(text: str) -> dict:
    # 프롬프트 + 텍스트 조합
    # OpenAI API 호출
    # 제목, 요약본 파싱 후 반환
    pass
```

---

### 6-8. routers/summarize.py

엔드포인트를 정의하고 서비스를 호출하는 파일입니다. 라우터는 로직 없이 서비스 호출만 합니다.

**[작성 가이드]**

```python
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
```

---

## 7. 서버 실행 방법

```bash
cd backend
uvicorn main:app --reload
```

서버 실행 후 브라우저에서 아래 주소로 접속하면 Swagger UI에서 API를 테스트할 수 있습니다.

```
http://localhost:8000/docs
```

---

## 8. API 엔드포인트 목록

| Method | URL                      | 설명                    |
| ------ | ------------------------ | ----------------------- |
| POST   | /summarize               | PDF 업로드 및 요약 요청 |
| GET    | /summaries               | 요약 목록 조회          |
| GET    | /summaries/{id}          | 요약 상세 조회          |
| GET    | /summaries/{id}/download | 요약본 TXT 다운로드     |
