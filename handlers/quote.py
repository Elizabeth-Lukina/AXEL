from telebot import types
from services.quote import get_quote
from db.queries import get_state


def register_quote_handlers(bot, get_main_menu):
    @bot.message_handler(func=lambda m: m.text == "🧠 Мысль дня")
    def send_quote(message):
        bot.send_message(message.chat.id, get_quote(), reply_markup=get_main_menu())
