import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    keyboard = [['Напоминание каждые 2 часа', 'Напоминание каждые 3 часа'], ['Отключить напоминания']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите режим напоминаний:', reply_markup=reply_markup)

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: CallbackContext):
    user_choice = update.message.text
    chat_id = update.message.chat_id

    if user_choice == 'Напоминание каждые 2 часа':
        context.job_queue.run_repeating(send_reminder, interval=7200, first=0, chat_id=chat_id, name=str(chat_id))
        await update.message.reply_text('Напоминания каждые 2 часа включены!')
    elif user_choice == 'Напоминание каждые 3 часа':
        context.job_queue.run_repeating(send_reminder, interval=10800, first=0, chat_id=chat_id, name=str(chat_id))
        await update.message.reply_text('Напоминания каждые 3 часа включены!')
    elif user_choice == 'Отключить напоминания':
        jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        for job in jobs:
            job.schedule_removal()
        await update.message.reply_text('Напоминания отключены.')

# Функция отправки напоминания
async def send_reminder(context: CallbackContext):
    job = context.job
    await context.bot.send_message(job.chat_id, text="Пора сходить на турник!")

# Основная функция
def main():
    # Вставьте свой токен сюда
    TOKEN = '7665287249:AAFkiu7s3_PKajwJeUvLbQ7KNZQrvJfH4mw'

    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()