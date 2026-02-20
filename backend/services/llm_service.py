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