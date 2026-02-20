# PDF 배치 요약 백엔드 (Gemini + MariaDB)

## 1. 개요
- 여러 PDF를 업로드하면 파일별로 순차 처리한다.
- 처리 파이프라인:
  - PDF 텍스트 추출
  - 텍스트 청킹
  - Gemini 임베딩 생성
  - Gemini 요약 생성
  - MariaDB 저장

## 2. 기술 스택
- FastAPI
- SQLAlchemy
- MariaDB (pymysql)
- PyPDF2
- Gemini REST API

## 3. 준비 사항
- Miniconda
- MariaDB
- Gemini API Key

## 4. 실행 준비

### 4-1. conda 환경
```bash
cd /Users/ijiyun/mini-project
conda create -n mini-project python=3.11 -y
conda activate mini-project
```

### 4-2. 패키지 설치
```bash
cd /Users/ijiyun/mini-project/backend
pip install -r requirements.txt
```

### 4-3. 환경변수 설정
```bash
cd /Users/ijiyun/mini-project/backend
cp .env.example .env
```

`.env` 예시:
```env
DATABASE_URL=mysql+pymysql://mini:mini1234!@127.0.0.1:3306/mini_project?charset=utf8mb4
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL_SUMMARY=gemini-2.0-flash
GEMINI_MODEL_EMBEDDING=text-embedding-004
MAX_UPLOAD_FILES=10
MAX_FILE_SIZE_MB=20
CHUNK_SIZE=1200
CHUNK_OVERLAP=200
```

### 4-4. DB 연결 확인
```bash
cd /Users/ijiyun/mini-project/backend
python -c "from database import engine; c=engine.connect(); print('DB OK'); c.close()"
```

## 5. 실행
```bash
cd /Users/ijiyun/mini-project/backend
uvicorn main:app --reload
```

Swagger:
- `http://127.0.0.1:8000/docs`

## 6. API

모든 엔드포인트는 `/api` prefix를 가진다.

- `POST /api/summarize/batch`
  - `multipart/form-data`, `files[]`
  - 여러 PDF를 순차 처리
- `GET /api/summaries`
  - 요약 목록 조회
- `GET /api/summaries/{id}`
  - 요약 상세 조회
- `GET /api/summaries/{id}/download`
  - 요약 txt 다운로드

## 7. 상태/에러 코드
- 상태: `PENDING`, `COMPLETED`, `FAILED`
- 대표 에러:
  - `INVALID_FILE`
  - `PDF_PARSE_FAILED`
  - `GEMINI_FAILED`
  - `NOT_FOUND`
  - `NOT_READY`

## 8. 프로젝트 구조
```text
backend/
├── main.py
├── database.py
├── requirements.txt
├── models/
│   └── summary.py
├── schemas/
│   └── summary.py
├── services/
│   ├── pdf_service.py
│   └── llm_service.py
├── prompts/
│   └── summarize_prompt.py
└── routers/
    └── summarize.py
```

## 9. 로컬 점검 명령어
```bash
cd /Users/ijiyun/mini-project/backend
python3 -m compileall .
```

## 10. API 스모크 테스트
```bash
cd /Users/ijiyun/mini-project/backend
PYTHONPATH=/Users/ijiyun/mini-project/backend /opt/homebrew/Caskroom/miniconda/base/envs/mini-project/bin/python scripts/smoke_test_api.py
```

정상일 때 확인 포인트:
- `LIST_STATUS 200`
- `BATCH_FAIL_STATUS 200` + `INVALID_FILE`
- `BATCH_OK_STATUS 200` + `COMPLETED`
- `DETAIL_STATUS 200`
- `DOWNLOAD_STATUS 200`

## 11. 통합 점검 순서
1. 백엔드 컴파일 확인
```bash
cd /Users/ijiyun/mini-project/backend
python3 -m compileall .
```
2. 백엔드 API 스모크 테스트
```bash
cd /Users/ijiyun/mini-project/backend
PYTHONPATH=/Users/ijiyun/mini-project/backend /opt/homebrew/Caskroom/miniconda/base/envs/mini-project/bin/python scripts/smoke_test_api.py
```
3. 프론트 QA 체크리스트 수행
- 문서: `/Users/ijiyun/mini-project/frontend/QA_CHECKLIST.md`
