
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext
from datetime import datetime, time
from ai_helpers import get_ai_tip

logger = logging.getLogger(__name__)

START_HOUR = 9
END_HOUR = 21

keyboard = [['Напоминание каждые 2 часа', 'Напоминание каждые 3 часа'],
            ['Отключить напоминания']]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def setup_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Выберите режим напоминаний:', reply_markup=reply_markup)

async def handle_message(update: Update, context: CallbackContext):
    user_choice = update.message.text
    chat_id = update.message.chat_id

    # Отключаем все старые напоминания для этого пользователя
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal()

    if user_choice == 'Напоминание каждые 2 часа':
        context.job_queue.run_repeating(reminder_job, interval=7200, first=0, chat_id=chat_id, name=str(chat_id), data={'interval': 2})
        await update.message.reply_text('Напоминания каждые 2 часа включены!', reply_markup=reply_markup)
    elif user_choice == 'Напоминание каждые 3 часа':
        context.job_queue.run_repeating(reminder_job, interval=10800, first=0, chat_id=chat_id, name=str(chat_id), data={'interval': 3})
        await update.message.reply_text('Напоминания каждые 3 часа включены!', reply_markup=reply_markup)
    elif user_choice == 'Отключить напоминания':
        await update.message.reply_text('Напоминания отключены.', reply_markup=reply_markup)

# Основная задача-напоминание
async def reminder_job(context: CallbackContext):
    now = datetime.now().time()
    if time(START_HOUR) <= now <= time(END_HOUR):
        chat_id = context.job.chat_id
        interval = context.job.data.get('interval', 2)

        await context.bot.send_message(chat_id, text="Пора сходить на турник! 💪")

        # Совет от ИИ – раз в 2 напоминания
        if not hasattr(context.job, "tip_count"):
            context.job.tip_count = 0

        if context.job.tip_count % 2 == 0:
            tip = await get_ai_tip()
            await context.bot.send_message(chat_id, text=f"💡 Советы по подтягиваниям: {tip}")

        context.job.tip_count += 1
