import os
import aiohttp

async def get_ai_tip():
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not hf_token:
        return "Сегодня главное — не пропустить тренировку!"

    url = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": "Дай интересный совет или мотивацию для подтягиваний для начинающих.",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=15) as resp:
                data = await resp.json()
                if isinstance(data, list) and data:
                    return data[0].get('generated_text', 'Сегодня главное — не пропустить тренировку!')
                else:
                    return "Сегодня главное — не пропустить тренировку!"
    except Exception as e:
        print(e)
        return "Сегодня главное — не пропустить тренировку!"
