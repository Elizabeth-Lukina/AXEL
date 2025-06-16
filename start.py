from telebot import types
from database import user_exists, set_state
from ui import get_main_menu


def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    def start(message):
        chat_id = message.chat.id
        username = message.from_user.username or 'неизвестно'
        if not user_exists(chat_id):
            bot.send_message(chat_id, f" ✌  Йоу, йоу, йоу! Привет {username}\n! "
                                      f"Я твой личный ассистент — AXIOM!\n"
                                      f"Точнее пока только учусь им быть, но постараюсь быть уже полезным")

            # Спросить о рассылке
            bot.send_message(message.chat.id, "Хочешь получать утреннюю рассылку?", reply_markup=markup)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("Да", "Нет")
            set_state(message.chat.id, "awaiting_subscription")

        else:
            bot.send_message(chat_id, "Мы же уже знакомы, чем займемся?", reply_markup=get_main_menu())
