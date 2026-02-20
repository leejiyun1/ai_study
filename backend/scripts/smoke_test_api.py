from fastapi.testclient import TestClient

from main import app
from routers import summarize as summarize_router


def run_smoke_test() -> int:
    with TestClient(app) as client:
        # 1) 목록 조회
        list_resp = client.get("/api/summaries")
        print("LIST_STATUS", list_resp.status_code)

        # 2) 실패 경로: 잘못된 파일 확장자
        bad_files = {"files": ("bad.txt", b"not pdf", "text/plain")}
        bad_resp = client.post("/api/summarize/batch", files=bad_files)
        print("BATCH_FAIL_STATUS", bad_resp.status_code)
        print("BATCH_FAIL_BODY", bad_resp.json())

        # 3) 성공 경로: 외부 API 의존성을 없애기 위해 서비스 모킹
        original_extract = summarize_router.pdf_service.extract_text
        original_split = summarize_router.pdf_service.split_text_into_chunks
        original_embed = summarize_router.llm_service.embed_chunks
        original_summarize = summarize_router.llm_service.summarize

        async def fake_extract(_file, max_file_size_bytes=None):
            return "테스트 원문 텍스트입니다."

        def fake_split(_text, chunk_size=1200, overlap=200):
            return ["테스트 원문", "텍스트입니다"]

        async def fake_embed(_chunks):
            return [[0.1, 0.2], [0.3, 0.4]]

        async def fake_summarize(_text):
            return {"title": "테스트 제목", "summary": "테스트 요약 본문"}

        summarize_router.pdf_service.extract_text = fake_extract
        summarize_router.pdf_service.split_text_into_chunks = fake_split
        summarize_router.llm_service.embed_chunks = fake_embed
        summarize_router.llm_service.summarize = fake_summarize

        try:
            good_files = {"files": ("good.pdf", b"%PDF-1.4\n%mock\n", "application/pdf")}
            ok_resp = client.post("/api/summarize/batch", files=good_files)
            print("BATCH_OK_STATUS", ok_resp.status_code)
            print("BATCH_OK_BODY", ok_resp.json())

            results = ok_resp.json().get("results", []) if ok_resp.status_code == 200 else []
            if not results:
                return 1

            doc_id = results[0]["document_id"]
            detail_resp = client.get(f"/api/summaries/{doc_id}")
            print("DETAIL_STATUS", detail_resp.status_code)
            print("DETAIL_BODY", detail_resp.json())

            download_resp = client.get(f"/api/summaries/{doc_id}/download")
            print("DOWNLOAD_STATUS", download_resp.status_code)
            print("DOWNLOAD_HEAD", download_resp.headers.get("content-disposition"))
            print("DOWNLOAD_TEXT", download_resp.text[:80])
        finally:
            summarize_router.pdf_service.extract_text = original_extract
            summarize_router.pdf_service.split_text_into_chunks = original_split
            summarize_router.llm_service.embed_chunks = original_embed
            summarize_router.llm_service.summarize = original_summarize

    return 0


if __name__ == "__main__":
    raise SystemExit(run_smoke_test())
