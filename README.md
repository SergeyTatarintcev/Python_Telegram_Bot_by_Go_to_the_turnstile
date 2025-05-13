Telegram Bot для напоминаний о тренировках
Этот Telegram-бот напоминает вам о тренировках на турнике через заданные интервалы времени. У него есть три режима:

Напоминание каждые 2 часа.
Напоминание каждые 3 часа.
Отключение напоминаний.
Требования
Для работы бота вам понадобится:

Python 3.8 или выше.
Библиотека python-telegram-bot.
Сервер (например, Beget) для размещения бота.
Установка и настройка
1. Клонируйте репозиторий
Склонируйте этот репозиторий на ваш сервер:

bash


1
2
git clone https://github.com/your_username/Python_Telegram_Bot_by_Go_to_the_turnstile.git 
cd Python_Telegram_Bot_by_Go_to_the_turnstile
2. Создайте виртуальное окружение
Создайте и активируйте виртуальное окружение:

bash


1
2
python3 -m venv .venv
source .venv/bin/activate
3. Установите зависимости
Установите необходимые библиотеки:

bash


1
pip install python-telegram-bot
4. Настройте токен бота
Откройте файл bot.py и замените значение переменной TOKEN на токен вашего бота:

python


1
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
Токен можно получить у @BotFather в Telegram.

5. Запустите бота
Запустите бота вручную:

bash


1
python bot.py
6. Настройте автоматический запуск через cron
Чтобы бот запускался автоматически при перезагрузке сервера, добавьте задачу в cron:

bash


1
crontab -e
Добавьте следующую строку:

bash


1
@reboot cd /path/to/Python_Telegram_Bot_by_Go_to_the_turnstile && source .venv/bin/activate && python bot.py >> /path/to/Python_Telegram_Bot_by_Go_to_the_turnstile/cron.log 2>&1 &
Замените /path/to/Python_Telegram_Bot_by_Go_to_the_turnstile на реальный путь к папке с ботом.

Структура проекта


1
2
3
4
5
6
Python_Telegram_Bot_by_Go_to_the_turnstile/
├── bot.py               # Основной код бота
├── .venv/               # Виртуальное окружение
├── cron.log             # Логи cron
├── README.md            # Документация проекта
└── .gitignore           # Файл для исключения ненужных файлов
Как это работает
Бот использует библиотеку python-telegram-bot для взаимодействия с Telegram API.
Пользователь может выбрать один из трех режимов напоминаний через кнопки в Telegram.
Напоминания отправляются через планировщик задач (apscheduler), который встроен в библиотеку.
Пример использования
Откройте Telegram и найдите своего бота.
Отправьте команду /start.
Выберите режим напоминаний:
"Напоминание каждые 2 часа".
"Напоминание каждые 3 часа".
"Отключить напоминания".
Лицензия
Этот проект распространяется под лицензией MIT .