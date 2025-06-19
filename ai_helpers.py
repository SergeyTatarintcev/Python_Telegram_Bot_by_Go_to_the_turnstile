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
                {"role": "user", "content":
                    "Дай уникальный, короткий совет или интересный мотивирующий факт для новичков по подтягиваниям. "
                    "Не повторяйся! Каждый раз формулируй по-новому. Не пиши советы, которые уже давал. "
                    "Формат: ‘Совет: ...’ или ‘Факт: ...’. До 250 символов."}
            ],
            max_tokens=100,  # Оптимально по опыту
            temperature=1.3,
        )
        tip = response.choices[0].message.content.strip()
        # Обрезаем до 250 символов, если вдруг OpenAI размахнётся
        if len(tip) > 250:
            tip = tip[:247] + "..."
        return tip
    except Exception as e:
        return f"❌ Ошибка при получении совета от ИИ: {e}"

async def get_ai_tip_async():
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, get_ai_tip)
