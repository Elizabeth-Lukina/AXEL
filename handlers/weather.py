from db.queries import get_state, clear_state, save_user, get_preferences, set_state, save_preferences
from services.weather import get_weather
from ui.ui import get_subscription_items_keyboard, get_main_menu

def register_weather_handlers(bot, get_main_menu):
    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_city")
    def handle_city_for_subscription(message):
        city = message.text.strip()
        chat_id = message.chat.id

        save_user(chat_id, city)
        clear_state(chat_id)

        prefs = get_preferences(chat_id) or []
        if "Погода" not in prefs:
            prefs.append("Погода")
            save_preferences(chat_id, prefs)

        bot.send_message(chat_id, f"🌆 Отлично, я запомнил твой город: {city}.")
        bot.send_message(chat_id, "Выбери, что ещё хочешь получать в рассылке:",
                         reply_markup=get_subscription_items_keyboard())
        set_state(chat_id, "awaiting_subscription_items")

    @bot.message_handler(commands=['weather'])
    def ask_city_for_weather(message):
        chat_id = message.chat.id
        bot.send_message(chat_id, "🌦 Введи город для прогноза погоды:")
        set_state(chat_id, "awaiting_weather_city")

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_weather_city")
    def handle_weather_city(message):
        city = message.text.strip()
        chat_id = message.chat.id

        weather_info = get_weather(city)
        clear_state(chat_id)
        bot.send_message(chat_id, weather_info, reply_markup=get_main_menu())
