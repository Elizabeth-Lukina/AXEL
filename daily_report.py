import sqlite3
from datetime import date
import logging
from config import TELEGRAM_TOKEN
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from db.queries import get_tasks

from quote import get_quote
from weather import get_weather
from currency import get_currency

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("daily_report")

# Создание экземпляров бота и планировщика
bot = telebot.TeleBot(TELEGRAM_TOKEN)
scheduler = BackgroundScheduler(timezone=pytz.timezone("Europe/Moscow"))
scheduler.start()

DB_PATH = "weatherbot.db"


def connect():
    return sqlite3.connect(DB_PATH)


def format_tasks(chat_id):
    tasks = get_tasks(chat_id)
    if not tasks:
        return "✅ На сегодня задач нет."
    return "📋 Задачи на сегодня:\n" + "\n".join(f"– {t}" for t in tasks)


def send_report(chat_id, city):
    try:
        parts = [
            get_weather(city),
            get_currency(),
            format_tasks(chat_id),
            get_quote()
        ]
        message = "\n\n".join(filter(None, parts))
        bot.send_message(chat_id, message)
        logger.info(f"[OK] Рассылка отправлена для {chat_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки {chat_id}: {e}")


def schedule_report_for_user(chat_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT city, send_hour, send_minute FROM users WHERE chat_id = ? AND daily_enabled = 1",
                    (chat_id,))
        user = cur.fetchone()

    if user:
        city, hour, minute = user
        try:
            scheduler.add_job(
                send_report,
                trigger="cron",
                hour=hour,
                minute=minute,
                args=[chat_id, city],
                id=f"report_{chat_id}",
                replace_existing=True
            )
            logger.info(f"[INFO] Обновлена рассылка для {chat_id} на {hour:02}:{minute:02}")
        except Exception as e:
            logger.error(f"Ошибка планирования отчета для {chat_id}: {e}")


def schedule_reports():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT chat_id, city, send_hour, send_minute FROM users WHERE daily_enabled = 1")
        users = cur.fetchall()

    for chat_id, city, hour, minute in users:
        try:
            scheduler.add_job(
                send_report,
                trigger="cron",
                hour=hour,
                minute=minute,
                args=[chat_id, city],
                id=f"report_{chat_id}",
                replace_existing=True
            )
            logger.info(f"[INFO] Запланирована рассылка для {chat_id} на {hour:02}:{minute:02}")
        except Exception as e:
            logger.error(f"Ошибка планирования отчета для {chat_id}: {e}")
