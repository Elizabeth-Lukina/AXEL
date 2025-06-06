from telebot import types

from daily_report import schedule_report_for_user
from quote import get_quote
from weather import get_weather
from currency import get_currency
from config import ADMIN_CHAT_ID
from analytics import log_usage, get_stats, get_city_chart
from database import save_user, user_exists, set_state, get_state, clear_state, update_user_time, connect, save_feedback


def register_handlers(bot):
    def get_main_menu():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            types.KeyboardButton("Погода"),
            types.KeyboardButton("Мысль дня"),
            types.KeyboardButton("Курс валют"),
            types.KeyboardButton("Добавить дело"),
            types.KeyboardButton("Изменить время рассылки"),
            types.KeyboardButton("Обратная связь")
        ]
        markup.add(*buttons)
        return markup

    @bot.message_handler(commands=["start"])
    def start(message):
        chat_id = message.chat.id
        if not user_exists(chat_id):
            bot.send_message(chat_id, "Привет ✌ Я твой личный ассистент! Напиши город откуда ты")
            set_state(chat_id, "awaiting_city")
        else:
            bot.send_message(chat_id, "Я тебя запомнил. Что делаем?", reply_markup=get_main_menu())

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_city")
    def save_city(message):
        city = message.text.strip()
        save_user(message.chat.id, city)
        clear_state(message.chat.id)
        bot.send_message(message.chat.id,
                         f"Отлично, я запомнил твой город: {city}.\nТеперь каждый день ты будешь получать сводку.",
                         reply_markup=get_main_menu())

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_weather_city")
    def handle_weather_city(message):
        weather = get_weather(message.text)
        clear_state(message.chat.id)
        bot.send_message(message.chat.id, weather, reply_markup=get_main_menu())

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_time")
    def save_send_time(message):
        try:
            time_str = message.text.strip()
            hour, minute = map(int, time_str.split(":"))

            if 0 <= hour < 24 and 0 <= minute < 60:
                update_user_time(message.chat.id, hour, minute)
                clear_state(message.chat.id)
                schedule_report_for_user(message.chat.id)
                bot.send_message(message.chat.id, f"Готово! Сводка теперь будет приходить в {hour:02}:{minute:02}.",
                                 reply_markup=get_main_menu())
            else:
                raise ValueError
        except:
            bot.send_message(message.chat.id, "Неверный формат времени. Попробуй снова, например 07:30",
                             reply_markup=get_main_menu())

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_feedback")
    def feedback_received(message):
        clear_state(message.chat.id)
        username = message.from_user.username or 'неизвестно'
        bot.send_message(message.chat.id, "Спасибо за идею! Я передал её разработчику")

        # Сохраняем в БД
        save_feedback(message.chat.id, username, message.text)

        # Пересылаем админу
        feedback_text = f"Новая обратная связь от @{username} ({message.chat.id}):\n\n{message.text}"
        bot.send_message(ADMIN_CHAT_ID, feedback_text)

    @bot.message_handler(content_types=["text"])
    def text_handler(message):
        text = message.text.lower()
        chat_id = message.chat.id

        actions = {
            "погода": lambda: (set_state(chat_id, "awaiting_weather_city"), bot.send_message(chat_id, "Введи город:")),
            "мысль дня": lambda: bot.send_message(chat_id, get_quote(), reply_markup=get_main_menu()),
            "курс валют": lambda: bot.send_message(chat_id, get_currency(), reply_markup=get_main_menu()),
            "добавить дело": lambda: bot.send_message(chat_id, "Функция добавления дел в разработке 🚰",
                                                      reply_markup=get_main_menu()),
            "изменить время рассылки": lambda: (set_state(chat_id, "awaiting_time"),
                                                bot.send_message(chat_id, "Введи время в формате ЧЧ:ММ",
                                                                 reply_markup=get_main_menu())),
            "обратная связь": lambda: (set_state(chat_id, "awaiting_feedback"),
                                       bot.send_message(chat_id,
                                                        "✉ Напиши, что бы ты хотел улучшить в боте. Я обязательно прочитаю!")
                                       )
        }

        if text in actions:
            actions[text]()
        else:
            bot.send_message(chat_id, "Я тебя не понял. Выбери действие из меню", reply_markup=get_main_menu())
