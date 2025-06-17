from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def get_ai_tip():
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Дай интересный совет по подтягиваниям или мотивирующий факт для новичков."}
            ],
            max_tokens=60,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Ошибка при получении совета от ИИ: {e}"

async def get_ai_tip_async():
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, get_ai_tip)
