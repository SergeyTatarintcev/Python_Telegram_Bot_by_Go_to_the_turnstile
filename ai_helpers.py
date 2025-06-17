from openai import OpenAI
import os

# Берём ключ из переменной окружения или .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Создаём клиента
client = OpenAI(api_key=OPENAI_API_KEY)

async def get_ai_tip():
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Дай интересный совет по подтягиваниям или мотивирующий факт для новичков."}
            ],
            max_tokens=60,
            temperature=0.7,
        )
        # В новой версии OpenAI message находится тут:
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Ошибка при получении совета от ИИ: {e}"
