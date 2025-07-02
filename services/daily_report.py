import logging
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

from db.init_db import connect
from db.queries import get_tasks, get_preferences
from services.quote import get_quote
from services.weather import get_weather
from services.currency import get_currency

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("daily_report")

scheduler = BackgroundScheduler(timezone=pytz.timezone("Europe/Moscow"))
scheduler.start()


def format_tasks(chat_id):
    tasks = get_tasks(chat_id)
    if not tasks:
        return "✅ На сегодня задач нет."
    return "📋 Задачи на сегодня:\n" + "\n".join(f"– {t}" for t in tasks)


def send_report(bot, chat_id, city):
    try:
        prefs = get_preferences(chat_id) or []
        parts = []

        if "Погода" in prefs:
            parts.append(get_weather(city))
        if "Курс валют" in prefs:
            parts.append(get_currency())
        if "Мысль дня" in prefs:
            parts.append(get_quote())

        parts.append(format_tasks(chat_id))  # Задачи показываем всегда

        message = "\n\n".join(filter(None, parts))
        bot.send_message(chat_id, message)
        logger.info(f"[OK] Рассылка отправлена для {chat_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки {chat_id}: {e}")


def schedule_report_for_user(bot, chat_id):
    """Запланировать рассылку только для одного пользователя"""
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT city, send_hour, send_minute FROM users WHERE chat_id = ? AND daily_enabled = 1",
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
                args=[bot, chat_id, city],  # Передаем bot, chat_id и city
                id=f"report_{chat_id}",
                replace_existing=True
            )
            logger.info(f"[INFO] Обновлена рассылка для {chat_id} на {hour:02}:{minute:02}")
        except Exception as e:
            logger.error(f"Ошибка планирования отчета для {chat_id}: {e}")


def schedule_reports(bot):
    """Запланировать рассылку для всех пользователей"""
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT chat_id, city, send_hour, send_minute FROM users WHERE daily_enabled = 1")
        users = cur.fetchall()

    for chat_id, city, hour, minute in users:
        try:
            scheduler.add_job(
                send_report,
                trigger="cron",
                hour=hour,
                minute=minute,
                args=[bot, chat_id, city],  # Передаем bot, chat_id и city
                id=f"report_{chat_id}",
                replace_existing=True
            )
            logger.info(f"[INFO] Запланирована рассылка для {chat_id} на {hour:02}:{minute:02}")
        except Exception as e:
            logger.error(f"Ошибка планирования отчета для {chat_id}: {e}")
