import os
import openai

async def get_ai_tip():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        return "Сегодня главное — не пропустить тренировку!"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — мотивационный тренер по подтягиваниям."},
                {"role": "user", "content": "Дай интересный совет или факт о подтягиваниях для начинающих."}
            ],
            max_tokens=60,
            temperature=0.7,
        )
        tip = response.choices[0].message['content'].strip()
        return tip
    except Exception as e:
        print(e)
        return "Сегодня главное — не пропустить тренировку!"
