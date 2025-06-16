from telebot import types

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
