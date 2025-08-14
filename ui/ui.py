from telebot import types


def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🌤 Погода", "💱 Курс валют")
    markup.add("🧠 Мысль дня", "⏰ Время рассылки")
    markup.add("📋 Планировщик", "🎲 Поиграем?")
    markup.add("📬 Обратная связь")
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

def get_menu_tasks():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📅 Задачи на сегодня", "🔙 Назад в главное меню")
    return markup
