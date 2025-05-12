import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Настройки
TOKEN = "ТВОЙ_ТОКЕН_ОТ_BOTFATHER"
CHAT_ID = None
scheduler = BackgroundScheduler()

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Клавиатура
keyboard = [
    ["Напоминать каждые 2 часа"],
    ["Напоминать каждые 3 часа"],
    ["Отключить напоминания"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Напоминалка
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=CHAT_ID, text="💪 Пора на турник! 💪")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    await update.message.reply_text(
        "Привет! Я буду напоминать тебе о турнике. Выбери интервал:",
        reply_markup=reply_markup
    )

# Обработка кнопок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    text = update.message.text

    if text == "Напоминать каждые 2 часа":
        scheduler.remove_all_jobs()
        scheduler.add_job(send_reminder, IntervalTrigger(hours=2), args=[context])
        await update.message.reply_text("✅ Буду напоминать каждые 2 часа!")

    elif text == "Напоминать каждые 3 часа":
        scheduler.remove_all_jobs()
        scheduler.add_job(send_reminder, IntervalTrigger(hours=3), args=[context])
        await update.message.reply_text("✅ Буду напоминать каждые 3 часа!")

    elif text == "Отключить напоминания":
        scheduler.remove_all_jobs()
        await update.message.reply_text("❌ Напоминания отключены.")

# main
def main():
    scheduler.start()
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()