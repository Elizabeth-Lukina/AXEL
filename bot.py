import telebot
from config import TELEGRAM_TOKEN
from handlers import register_handlers
from database import init_db
from daily_report import schedule_reports  # импортируем, но вызываем вручную

# Инициализация базы
init_db()

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)
register_handlers(bot)

# Планирование рассылок
schedule_reports()


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
