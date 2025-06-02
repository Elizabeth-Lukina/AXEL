from telebot import types
from weather import get_weather
from analytics import log_usage, get_stats, get_city_chart

def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(message.chat.id, "Привет ✌ Я твой личный ассистент! Напиши город откуда ты.")
        log_usage(message.chat.id, "/start")

    @bot.message_handler(commands=["stats"])
    def stats(message):
        log_usage(message.chat.id, "/stats")
        stats_text = get_stats()
        bot.send_message(message.chat.id, stats_text)

    @bot.message_handler(commands=["chart"])
    def chart(message):
        log_usage(message.chat.id, "/chart")
        chart_path = get_city_chart()
        with open(chart_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

    @bot.message_handler(content_types=["text"])
    def text_handler(message):
        log_usage(message.chat.id, "weather_query", extra=message.text)
        weather = get_weather(message.text)
        bot.send_message(message.chat.id, weather)

    @bot.message_handler(commands=['my_stats'])
    def my_stats(message):
        log_usage(message.chat.id, '/my_stats')
        stats_text = get_task_stats(message.chat.id)
        bot.send_message(message.chat.id, stats_text)
