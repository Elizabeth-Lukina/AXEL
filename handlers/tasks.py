from telebot import types
from db.queries import set_state, get_state, clear_state, add_task, get_tasks
from ui.ui import get_main_menu

def register_task_handlers(bot):

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_task_text")
    def save_task(message):
        chat_id = message.chat.id
        task_text = message.text.strip()
        print(f"[DEBUG] save_task called with task_text: '{task_text}'")

        if not task_text:
            bot.send_message(chat_id, "⚠️ Пустая задача? Пожалуйста, введи текст задачи.")
            return

        try:
            print("[DEBUG] Попытка добавить задачу в БД")
            add_task(chat_id, task_text)
            print("[DEBUG] Задача добавлена в БД успешно")
            clear_state(chat_id)
            bot.send_message(chat_id, f"✅ Задача добавлена: «{task_text}»", reply_markup=get_main_menu())
        except Exception as e:
            print(f"[ERROR] Ошибка при добавлении задачи: {e}")
            bot.send_message(chat_id, "⚠️ Произошла ошибка при добавлении задачи.")

    @bot.message_handler(func=lambda m: m.text == "📋 Мои задачи")
    def show_tasks(message):
        chat_id = message.chat.id
        clear_state(chat_id)
        tasks = get_tasks(chat_id)
        if tasks:
            text = "🗂 *Твои задачи на сегодня:*\n" + "\n".join([f"• {t}" for t in tasks])
        else:
            text = "📭 У тебя пока нет задач на сегодня."
        bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=get_main_menu())
