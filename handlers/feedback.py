from telebot import types
from db.queries import clear_state, save_feedback
from config import ADMIN_CHAT_ID
from db.queries import get_state


def register_feedback_handlers(bot):
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
