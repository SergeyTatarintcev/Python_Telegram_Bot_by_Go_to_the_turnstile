import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, PersistenceInput, PicklePersistence

# Вставь сюда свой ТОКЕН, который дал BotFather
TOKEN = "7665287249:AAFkiu7s3_PKajwJeUvLbQ7KNZQrvJfH4mw" # <--- ЗАМЕНИ ЭТО НА СВОЙ ТОКЕН!!!

# Настройка логирования, чтобы видеть, что делает бот
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Файл для сохранения состояния (какой интервал выбран)
PERSISTENCE_FILE = "bot_persistence.pickle"

# Функция, которая будет отправлять напоминание
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id
    try:
        await context.bot.send_message(chat_id=chat_id, text="💪 Пора на турник! Время подтягиваться!")
        logger.info(f"Отправлено напоминание в чат {chat_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке напоминания в чат {chat_id}: {e}")
        # Если ошибка связана с тем, что пользователь заблокировал бота,
        # можно удалить задачу, чтобы не пытаться слать снова
        if "bot was blocked" in str(e).lower() or "chat not found" in str(e).lower():
            logger.info(f"Пользователь {chat_id} заблокировал бота или чат не найден. Удаляем задачу.")
            job.schedule_removal()
            # Также очистим user_data, если нужно
            if 'reminder_interval_hours' in context.user_data:
                del context.user_data['reminder_interval_hours']


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    logger.info(f"Пользователь {user.first_name} (ID: {user.id}, Chat_ID: {chat_id}) запустил бота.")

    keyboard = [
        [InlineKeyboardButton("Напоминание каждые 2 часа", callback_data='set_2_hours')],
        [InlineKeyboardButton("Напоминание каждые 3 часа", callback_data='set_3_hours')],
        [InlineKeyboardButton("Отключить напоминания", callback_data='disable_reminders')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    current_interval = context.user_data.get('reminder_interval_hours')
    message_text = f"Привет, {user.mention_html()}! Я помогу тебе не забывать про турник.\n"
    if current_interval:
        message_text += f"Сейчас напоминания установлены на каждые {current_interval} часа(ов)."
    else:
        message_text += "Сейчас напоминания отключены."
    message_text += "\n\nВыбери опцию:"

    await update.message.reply_html(message_text, reply_markup=reply_markup)

# Функция для удаления существующих задач напоминаний для пользователя
def remove_existing_job(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    # Имя задачи должно быть уникальным для каждого пользователя, например, 'reminder_job_{chat_id}'
    job_name = f'reminder_job_{chat_id}'
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    if current_jobs:
        for job in current_jobs:
            job.schedule_removal()
        logger.info(f"Удалены предыдущие задачи напоминаний для чата {chat_id}")
    return job_name

# Обработчик нажатий на кнопки
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Обязательно, чтобы кнопка перестала "грузиться"

    chat_id = query.message.chat_id
    action = query.data

    # Удаляем старые задачи перед установкой новой
    job_name = remove_existing_job(chat_id, context)

    interval_hours = None
    message = ""

    if action == 'set_2_hours':
        interval_hours = 2
        interval_seconds = 2 * 60 * 60 # 2 часа в секундах
        context.job_queue.run_repeating(send_reminder, interval=interval_seconds, first=0, chat_id=chat_id, name=job_name)
        message = "Хорошо! Буду напоминать каждые 2 часа."
        logger.info(f"Установлено напоминание каждые 2 часа для чата {chat_id}")
    elif action == 'set_3_hours':
        interval_hours = 3
        interval_seconds = 3 * 60 * 60 # 3 часа в секундах
        context.job_queue.run_repeating(send_reminder, interval=interval_seconds, first=0, chat_id=chat_id, name=job_name)
        message = "Принято! Напоминания каждые 3 часа."
        logger.info(f"Установлено напоминание каждые 3 часа для чата {chat_id}")
    elif action == 'disable_reminders':
        # Задачи уже удалены функцией remove_existing_job
        message = "Напоминания отключены. Молодец, что занимался!"
        logger.info(f"Напоминания отключены для чата {chat_id}")
        interval_hours = None # Явно указываем, что интервал сброшен

    # Сохраняем выбор пользователя
    if interval_hours is not None:
        context.user_data['reminder_interval_hours'] = interval_hours
    elif 'reminder_interval_hours' in context.user_data:
        del context.user_data['reminder_interval_hours']

    await query.edit_message_text(text=message)


def main():
    # Создаем PicklePersistence
    # Убедимся, что директория для файла персистентности существует, если нет, создадим
    persistence_dir = os.path.dirname(PERSISTENCE_FILE)
    if persistence_dir and not os.path.exists(persistence_dir):
        os.makedirs(persistence_dir, exist_ok=True)

    # Если файл не существует, PicklePersistence может выдать ошибку при первой загрузке,
    # особенно если мы пытаемся загрузить 'user_data' и т.д. до того, как что-то сохранено.
    # Мы можем использовать PersistenceInput для инициализации, если это необходимо.
    persistence = PicklePersistence(filepath=PERSISTENCE_FILE,
                                    store_data=PersistenceInput(user_data=True, chat_data=False, bot_data=False, callback_data=True))


    # Создаем "мозг" бота
    application = Application.builder().token(TOKEN).persistence(persistence).build()

    # Добавляем обработчики команд и кнопок
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Запуск бота (он начинает слушать сообщения)
    logger.info("Бот запускается...")
    application.run_polling()

if __name__ == "__main__":
    main()