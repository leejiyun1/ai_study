# Frontend QA Checklist

## 1. Environment
- [ ] `node -v` 정상 출력
- [ ] `npm -v` 정상 출력
- [ ] `.env` 파일 존재 (`VITE_API_BASE_URL=/api`)

## 2. Build
```bash
cd /Users/ijiyun/mini-project/frontend
npm run build
```
- [ ] 빌드 성공 (`dist/` 생성)

## 3. Backend Connectivity
- [ ] 백엔드 실행: `uvicorn main:app --reload` (`127.0.0.1:8000`)
- [ ] 프론트 실행: `npm run dev` (`127.0.0.1:5173`)
- [ ] 업로드 페이지에서 PDF 업로드 후 완료/실패 메시지 확인
- [ ] 업로드 성공 시 검색 페이지 자동 이동 확인
- [ ] 검색 페이지에서 목록 자동 새로고침 확인

## 4. API Flow
- [ ] 목록 조회: `/api/summaries`
- [ ] 상세 조회: `/api/summaries/{id}`
- [ ] 다운로드: `/api/summaries/{id}/download`

## 5. Error Handling
- [ ] 비 PDF 업로드 시 `INVALID_FILE` 처리 확인
- [ ] 요약 준비 전 다운로드 시 `NOT_READY` 처리 확인

## 6. Regression Notes
- 2026-02-20: Node/Homebrew `simdjson` 링크 이슈 발생
- 복구 명령:
```bash
brew reinstall simdjson
brew reinstall node
```
