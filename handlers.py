from telebot import types

from daily_report import schedule_reports
from quote import get_quote
from weather import get_weather
from currency import get_currency
from analytics import log_usage, get_stats, get_city_chart
from database import save_user, user_exists, set_state, get_state, clear_state, update_user_time


def register_handlers(bot):
    def send_main_menu(chat_id, text):
        markup = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton("Погода", callback_data="weather"),
            types.InlineKeyboardButton("Мысль дня", callback_data="thought"),
            types.InlineKeyboardButton("Курс валют", callback_data="currency"),
            types.InlineKeyboardButton("Добавить дело", callback_data="add_task"),
            types.InlineKeyboardButton("Изменить время рассылки", callback_data="set_time")
        ]
        for button in buttons:
            markup.add(button)
        bot.send_message(chat_id, text, reply_markup=markup)

    @bot.message_handler(commands=["start"])
    def start(message):
        chat_id = message.chat.id
        if not user_exists(chat_id):
            bot.send_message(chat_id, "Привет ✌ Я твой личный ассистент! Напиши город откуда ты")
            set_state(chat_id, "awaiting_city")
        else:
            send_main_menu(chat_id, "Я тебя запомнил. Выбери действие ниже:")

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_city")
    def save_city(message):
        print("[DEBUG] Сработал save_city")
        city = message.text.strip()
        save_user(message.chat.id, city)
        print(f"[DEBUG] Сохранили город: {city}")
        clear_state(message.chat.id)
        print("[DEBUG] Сбросили состояние")
        bot.send_message(message.chat.id,
                         f"Отлично, я запомнил твой город: {city}.\nТеперь каждый день в 07:30 по МСК ты будешь получать сводку.")
        send_main_menu(message.chat.id, "Чем займёмся?")

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_weather_city")
    def handle_weather_city(message):
        weather = get_weather(message.text)
        clear_state(message.chat.id)
        bot.send_message(message.chat.id, weather)
        send_main_menu(message.chat.id, "Вот прогноз. Что дальше?")

    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        chat_id = call.message.chat.id
        data = call.data
        log_usage(chat_id, f"callback:{data}")
        bot.answer_callback_query(call.id)  # ✅ ОБЯЗАТЕЛЕН для inline-кнопок

        actions = {
            "weather": lambda: (
                set_state(chat_id, "awaiting_weather_city"),
                bot.send_message(chat_id, "Введи город для прогноза:")
            ),
            "currency": lambda: bot.send_message(chat_id, get_currency()),
            "thought": lambda: bot.send_message(chat_id, get_quote()),
            "add_task": lambda: bot.send_message(chat_id, "Функция добавления дел в разработке 🛠"),
            "set_time": lambda: (
                set_state(chat_id, "awaiting_time"),
                bot.send_message(chat_id,
                                 "Во сколько присылать утреннюю сводку? Введи время в формате ЧЧ:ММ, например 08:15.")
            )
        }

        if data in actions:
            actions[data]()

    @bot.message_handler(commands=["stats"])
    def stats(message):
        log_usage(message.chat.id, "/stats")
        stats_text = get_stats(message.chat.id)
        bot.send_message(message.chat.id, stats_text)

    @bot.message_handler(commands=["chart"])
    def chart(message):
        log_usage(message.chat.id, "/chart")
        chart_path = get_city_chart()
        with open(chart_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

    @bot.message_handler(commands=["set_time"])
    def ask_send_time(message):
        bot.send_message(message.chat.id,
                         "Во сколько присылать утреннюю сводку? Введи время в формате ЧЧ:ММ, например 08:15.")
        set_state(message.chat.id, "awaiting_time")

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_time")
    def save_send_time(message):
        try:
            time_str = message.text.strip()
            hour, minute = map(int, time_str.split(":"))

            if 0 <= hour < 24 and 0 <= minute < 60:
                update_user_time(message.chat.id, hour, minute)
                clear_state(message.chat.id)
                bot.send_message(message.chat.id, f"Готово! Сводка теперь будет приходить в {hour:02}:{minute:02}.")
            else:
                raise ValueError
        except:
            bot.send_message(message.chat.id, "Неверный формат времени, попробуй снова, например 07:30")

    # @bot.message_handler(commands=['my_stats'])
    # def my_stats(message):
    #     log_usage(message.chat.id, '/my_stats')
    #     stats_text = get_task_stats(message.chat.id)
    #     bot.send_message(message.chat.id, stats_text)
