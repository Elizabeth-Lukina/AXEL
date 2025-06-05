import sqlite3
from datetime import date
import logging
from config import TELEGRAM_TOKEN, OWM_API_KEY
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

from quote import get_quote
from weather import get_weather
from currency import get_currency
from database import init_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация базы данных
init_db()

# Создание экземпляров бота и планировщика
bot = telebot.TeleBot(TELEGRAM_TOKEN)
scheduler = BackgroundScheduler(timezone=pytz.timezone("Europe/Moscow"))
scheduler.start()

DB_PATH = "weatherbot.db"

def connect():
    return sqlite3.connect(DB_PATH)

def get_tasks(chat_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT task FROM tasks WHERE chat_id=? AND due_date=?", (chat_id, date.today()))
        rows = cur.fetchall()

    if not rows:
        return "✅ На сегодня задач нет."
    return "📋 Задачи на сегодня:\n" + "\n".join(f"— {row[0]}" for row in rows)

def send_report(chat_id, city):
    try:
        parts = [
            get_weather(city),
            get_currency(),
            get_tasks(chat_id),
            get_quote()
        ]
        message = "\n\n".join(filter(None, parts))  # Убираем пустые части сообщения
        bot.send_message(chat_id, message)
        logger.info(f"[DEBUG] отправка рассылки для {chat_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки {chat_id}: {e}")

def schedule_reports():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT chat_id, city, send_hour, send_minute FROM users WHERE daily_enabled=1")
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
        except Exception as e:
            logger.error(f"Ошибка планирования отчета для {chat_id}: {e}")

