from telebot import types
from db.queries import get_state, clear_state, save_user
from services.weather import get_weather


def register_weather_handlers(bot, get_main_menu):
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
        bot.send_message(message.chat_id, weather, reply_markup=get_main_menu())
