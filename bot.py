import telebot
from config import TELEGRAM_TOKEN
from handlers import register_handlers
from daily_report import send_daily_reports
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

bot = telebot.TeleBot(TELEGRAM_TOKEN)
register_handlers(bot)

# Планировщик: ежедневная рассылка в 07:30 по МСК
scheduler = BackgroundScheduler(timezone=pytz.timezone("Europe/Moscow"))
scheduler.add_job(send_daily_reports, CronTrigger(hour=7, minute=30))
scheduler.start()

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
