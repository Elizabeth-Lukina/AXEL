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


def get_yes_no_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("✅ Да", "❌ Нет")
    return markup


def get_subscription_items_keyboard():
    valid_items = ["🌤 Погода", "💱 Курс валют", "🧠 Мысль дня"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item in valid_items:
        markup.add(item)
    markup.add("✅ Готово")
    return markup


