import telebot
from config import TELEGRAM_TOKEN
from handlers import register_handlers
from db.init_db import init_db
from daily_report import schedule_reports  # импортируем, но вызываем вручную
from start import register_handlers_start

# 1. Сначала база
init_db()

# 2. Затем бот
bot = telebot.TeleBot(TELEGRAM_TOKEN)
register_handlers_start(bot)
register_handlers(bot)

# 3. Затем расписание (и только один раз!)
schedule_reports(bot)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling(none_stop=True)

