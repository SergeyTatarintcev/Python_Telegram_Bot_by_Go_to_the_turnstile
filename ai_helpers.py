import httpx
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def get_ai_tip():
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {"role": "user", "content": "Дай интересный совет по подтягиваниям или мотивирующий факт для новичков."}
        ],
        "max_tokens": 60,
        "temperature": 0.7,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30,
        )
        r = response.json()
        return (
            r.get("choices", [{}])[0].get("message", {}).get("content", "🤖 Не удалось получить совет.")
        )
