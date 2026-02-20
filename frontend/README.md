# Frontend (React + Vite)

## 1. 개요
- 백엔드 `/api` 엔드포인트와 연동되는 프론트 UI
- 주요 화면:
  - 업로드 (`/upload`)
  - 검색/조회 (`/search`)

## 2. 실행
```bash
cd /Users/ijiyun/mini-project/frontend
npm install
cp .env.example .env
npm run dev
```

기본 접속:
- `http://127.0.0.1:5173`

## 3. 환경 변수
`.env`:
```env
VITE_API_BASE_URL=/api
```

## 4. 개발 프록시
Vite dev server에서 `/api` 요청은 백엔드로 프록시된다.

```js
server: {
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    },
  },
}
```

## 5. 백엔드 연동 포인트
- `POST /api/summarize/batch`
- `GET /api/summaries`
- `GET /api/summaries/{id}`
- `GET /api/summaries/{id}/download`

## 6. 참고
- 로컬에서 백엔드가 먼저 실행되어 있어야 업로드/조회가 정상 동작한다.
