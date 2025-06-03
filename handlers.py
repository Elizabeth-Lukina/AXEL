from telebot import types
from weather import get_weather
from analytics import log_usage, get_stats, get_city_chart
from database import save_user, user_exists, set_state, get_state, clear_state


def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Погода")
        btn2 = types.KeyboardButton("Мысль дня")
        btn3 = types.KeyboardButton("Курс валют")
        btn4 = types.KeyboardButton("Добавить дело")
        markup.add(btn1, btn2, btn3, btn4, )
        chat_id = message.chat.id
        if not user_exists(chat_id):
            bot.send_message(message.chat.id, "Привет ✌ Я твой личный ассистент! Напиши город откуда ты", reply_markup=markup)
            set_state(chat_id, "awaiting_city")
        else:
            bot.send_message(chat_id,
                             "Ты уже зарегистрирован. Используй /weather для прогноза или жди утреннюю рассылку.")

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_city")
    def save_city(message):
        city = message.text.strip()
        save_user(message.chat.id, city)
        clear_state(message.chat.id)
        bot.send_message(message.chat.id,
                         f"Отлично, я запомнил твой город: {city}.\nТеперь каждый день в 07:30 по МСК ты будешь получать сводку.")

    @bot.message_handler(commands=['weather'])
    def weather(message):
        bot.send_message(message.chat.id, "Введи город для прогноза:")
        set_state(message.chat.id, "awaiting_weather_city")

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

    # @bot.message_handler(commands=['my_stats'])
    # def my_stats(message):
    #     log_usage(message.chat.id, '/my_stats')
    #     stats_text = get_task_stats(message.chat.id)
    #     bot.send_message(message.chat.id, stats_text)
