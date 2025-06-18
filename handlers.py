import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext
from datetime import datetime, time
from ai_helpers import get_ai_tip_async

logger = logging.getLogger(__name__)

START_HOUR = 9
END_HOUR = 21

keyboard = [
    ['Напоминание каждые 2 часа', 'Напоминание каждые 3 часа'],
    ['Отключить напоминания']
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def setup_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Handlers initialized")

async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    logger.info(f"[START] Пользователь {chat_id} запустил бота")
    await update.message.reply_text('Выберите режим напоминаний:', reply_markup=reply_markup)

async def handle_message(update: Update, context: CallbackContext):
    user_choice = update.message.text
    chat_id = update.message.chat_id

    logger.info(f"[CHOICE] Пользователь {chat_id} выбрал: {user_choice}")

    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if jobs:
        logger.info(f"[REMOVE JOBS] Удаляем старые напоминания для пользователя {chat_id} ({len(jobs)} шт.)")
    for job in jobs:
        job.schedule_removal()

    if user_choice == 'Напоминание каждые 2 часа':
        context.job_queue.run_repeating(
            reminder_job,
            interval=7200,
            first=0,
            chat_id=chat_id,
            name=str(chat_id),
            data={'interval': 2, 'tip_count': 0}
        )
        logger.info(f"[SET REMINDER] Пользователь {chat_id}: Напоминания каждые 2 часа")
        await update.message.reply_text('Напоминания каждые 2 часа включены!', reply_markup=reply_markup)
    elif user_choice == 'Напоминание каждые 3 часа':
        context.job_queue.run_repeating(
            reminder_job,
            interval=10800,
            first=0,
            chat_id=chat_id,
            name=str(chat_id),
            data={'interval': 3, 'tip_count': 0}
        )
        logger.info(f"[SET REMINDER] Пользователь {chat_id}: Напоминания каждые 3 часа")
        await update.message.reply_text('Напоминания каждые 3 часа включены!', reply_markup=reply_markup)
    elif user_choice == 'Отключить напоминания':
        logger.info(f"[DISABLE REMINDER] Пользователь {chat_id} отключил напоминания")
        await update.message.reply_text('Напоминания отключены.', reply_markup=reply_markup)
    else:
        logger.info(f"[UNKNOWN CHOICE] Пользователь {chat_id} выбрал неизвестную опцию: {user_choice}")
        await update.message.reply_text('Неизвестная команда. Пожалуйста, выберите режим напоминаний.', reply_markup=reply_markup)

async def reminder_job(context: CallbackContext):
    now = datetime.now().time()
    chat_id = context.job.chat_id
    data = context.job.data

    if time(START_HOUR) <= now <= time(END_HOUR):
        logger.info(f"[REMINDER] Отправлено напоминание пользователю {chat_id}")
        await context.bot.send_message(chat_id, text="Пора сходить на турник! 💪")

        tip_count = data.get('tip_count', 0)
        if tip_count % 2 == 0:
            logger.info(f"[AI TIP] Получаем совет для пользователя {chat_id}")
            tip = await get_ai_tip_async()
            await context.bot.send_message(chat_id, text=f"💡 Советы по подтягиваниям: {tip}")

        data['tip_count'] = tip_count + 1
        context.job.data = data
    else:
        logger.info(f"[SILENT HOURS] Напоминание для пользователя {chat_id} не отправлено (ночное время)")
