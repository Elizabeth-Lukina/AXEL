from telebot import types
from db.queries import (
    set_state, get_state, clear_state,
    add_task, get_tasks
)
from ui.ui import get_main_menu
from handlers.nlp_task_handler import handle_free_text


def register_task_handlers(bot, parse_intent):

    # Кнопка: "📝 Добавить дело"
    @bot.message_handler(func=lambda m: m.text == "📝 Добавить дело")
    def ask_task_text(message):
        chat_id = message.chat.id
        set_state(chat_id, "awaiting_task_text")
        bot.send_message(chat_id, "✍️ Введи текст новой задачи:")

    # Кнопка: "📋 Мои задачи"
    @bot.message_handler(func=lambda m: m.text == "📋 Мои задачи")
    def show_tasks(message):
        chat_id = message.chat.id
        clear_state(chat_id)
        tasks = get_tasks(chat_id)
        if tasks:
            text = "🗂 *Твои задачи:*\n" + "\n".join([f"• {t}" for t in tasks])
        else:
            text = "📭 У тебя пока нет задач."
        bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=get_main_menu())

    # Состояние: ожидание текста задачи
    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_task_text")
    def save_task(message):
        chat_id = message.chat.id
        task_text = message.text.strip()
        print(f"[DEBUG] save_task called with task_text: '{task_text}'")

        if not task_text:
            bot.send_message(chat_id, "⚠️ Пустая задача? Введи текст снова.")
            return

        try:
            print("[DEBUG] Попытка добавить задачу в БД")
            add_task(chat_id, task_text)
            print("[DEBUG] Задача добавлена в БД")
            clear_state(chat_id)
            bot.send_message(chat_id, f"✅ Задача добавлена: «{task_text}»", reply_markup=get_main_menu())
        except Exception as e:
            print(f"[ERROR] Ошибка при добавлении задачи: {e}")
            bot.send_message(chat_id, "⚠️ Ошибка при добавлении задачи.")

    # # Обработка всех других сообщений — NLP
    # @bot.message_handler(func=lambda m: True)
    # def handle_any_text(message):
    #     user_id = message.chat.id
    #     user_text = message.text.strip()
    #     print(f"[DEBUG] handle_any_text: '{user_text}'")
    #
    #     try:
    #         result = parse_intent(user_text)
    #         intent = result.get("intent")
    #         entities = result.get("entities", {})
    #
    #         print(f"[DEBUG] parse_intent: '{user_text}' → intent: {intent}, entities: {entities}")
    #
    #         if intent == "add_task":
    #             task_text = entities.get("task") or user_text
    #             add_task(user_id, task_text)
    #             bot.send_message(user_id, f"🆕 Задача добавлена: «{task_text}»", reply_markup=get_main_menu())
    #
    #         elif intent == "list_tasks":
    #             tasks = get_tasks(user_id)
    #             if tasks:
    #                 text = "🗂 *Твои задачи:*\n" + "\n".join([f"• {t}" for t in tasks])
    #             else:
    #                 text = "📭 У тебя пока нет задач."
    #             bot.send_message(user_id, text, parse_mode="Markdown", reply_markup=get_main_menu())
    #
    #         else:
    #             print("[DEBUG] Неопределённый интент — передаём в NLP-хендлер")
    #             handle_free_text(bot, message, user_id)
    #
    #     except Exception as e:
    #         print(f"[ERROR] Ошибка при NLP-анализе: {e}")
    #         handle_free_text(bot, message, user_id)
