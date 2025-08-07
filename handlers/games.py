from telebot import types
from services.quote import get_quote
from db.queries import get_state


def register_game_handlers(bot, get_main_menu):
    @bot.message_handler(func=lambda m: m.text == "🎲 Поиграем?")
    def send_game(message):
        bot.send_message(message.chat.id, "Функция в разработке", reply_markup=get_main_menu())
