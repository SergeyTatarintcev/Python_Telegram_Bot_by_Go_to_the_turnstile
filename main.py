import os
from dotenv import load_dotenv
import logging
from telegram.ext import Application
from handlers import setup_handlers

def main():
    # Логирование (INFO выводит твои логи из handlers.py)
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=logging.INFO
    )

    load_dotenv()
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN не найден в .env!")
        return

    application = Application.builder().token(TOKEN).build()
    setup_handlers(application)

    print("Бот запущен! Жми Ctrl+C для остановки.")
    application.run_polling()

if __name__ == "__main__":
    main()
