from telebot import types
from db.queries import get_state, set_state


def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        types.KeyboardButton("🌤 Погода"),
        types.KeyboardButton("💱 Курс валют")
    )
    markup.row(
        types.KeyboardButton("🧠 Мысль дня"),
        types.KeyboardButton("📝 Добавить дело")
    )
    markup.row(
        types.KeyboardButton("⏰ Время рассылки"),
        types.KeyboardButton("📬 Обратная связь")
    )
    return markup


def register_main_menu_handlers(bot):
    @bot.message_handler(content_types=["text"])
    def text_handler(message):
        text = message.text.strip()
        chat_id = message.chat.id

        # Поведение при выборе пункта меню
        actions = {
            "🌤 Погода": lambda: (set_state(chat_id, "awaiting_weather_city"),
                                 bot.send_message(chat_id, "Введи город:")),
            "💱 Курс валют": lambda: bot.send_message(chat_id, get_currency(), reply_markup=get_main_menu()),
            "🧠 Мысль дня": lambda: bot.send_message(chat_id, get_quote(), reply_markup=get_main_menu()),
            "📝 Добавить дело": lambda: bot.send_message(chat_id, "Функция добавления дел в разработке 🚰",
                                                        reply_markup=get_main_menu()),
            "⏰ Время рассылки": lambda: (set_state(chat_id, "awaiting_time"),
                                         bot.send_message(chat_id, "Введи время в формате ЧЧ:ММ",
                                                          reply_markup=get_main_menu())),
            "📬 Обратная связь": lambda: (set_state(chat_id, "awaiting_feedback"),
                                         bot.send_message(chat_id,
                                                          "✉ Напиши, что бы ты хотел улучшить в боте. Я обязательно прочитаю!"))
        }

        # Особая логика для обратной связи
        if get_state(chat_id) == "awaiting_feedback":
            from db.queries import clear_state, save_feedback
            clear_state(chat_id)
            username = message.from_user.username or 'неизвестно'
            bot.send_message(chat_id, "Спасибо за идею! Я передал её разработчику")
            save_feedback(chat_id, username, text)
            from config import ADMIN_CHAT_ID
            bot.send_message(ADMIN_CHAT_ID, f"Новая обратная связь от @{username} ({chat_id}):\n\n{text}")
            return None

        if text in actions:
            actions[text]()
