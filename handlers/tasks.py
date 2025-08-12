from telebot import types
from db.queries import (
    add_task, delete_task, reschedule_task,
    get_tasks, mark_task_completed
)
from db.queries import set_state, get_state, clear_state
from tabulate import tabulate


def register_task_handlers(bot, parse_intent):
    @bot.message_handler(func=lambda m: m.text == "📋 Планировщик")
    def enter_task_mode(message):
        chat_id = message.chat.id
        set_state(chat_id, "awaiting_task_text")
        bot.send_message(chat_id, "Ты находишься в режиме планирования задач. Что будем делать?")

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_task_text")
    def handle_task_commands(message):
        chat_id = message.chat.id
        user_text = message.text.strip()

        try:
            result = parse_intent(user_text)
            intent = result.get("intent")
            task_text = result.get("task", "")
            date = result.get("date")

            if intent == "add_task":
                add_task(chat_id, task_text, intent, date)
                bot.send_message(chat_id, f"✅ Добавлена задача: «{task_text}»")

            elif intent == "delete_task":
                success = delete_task(chat_id, task_text)
                bot.send_message(chat_id, f"❌ Удалена: «{task_text}»" if success else "⚠️ Задача не найдена.")

            elif intent == "reschedule_task":
                success = reschedule_task(chat_id, task_text, date)
                bot.send_message(chat_id, f"🔁 Перенесена на {date.date()}" if success else "⚠️ Не удалось перенести.")

            elif intent == "list_tasks":
                send_task_list(bot, chat_id)

            elif intent == "mark_task_completed":
                task_id = int(result.get("task", "").strip())
                success = mark_task_completed(chat_id, task_id)
                bot.send_message(chat_id,
                                 f"✅ Задача {task_id} отмечена как выполненная" if success else "⚠️ Не удалось отметить.")

            else:
                bot.send_message(chat_id, "🤔 Не понял команду. Попробуй снова.")

        except Exception as e:
            print(f"[ERROR] {e}")
            bot.send_message(chat_id, "Ошибка при обработке команды.")

        finally:
            clear_state(chat_id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("complete:"))
    def handle_complete_task(call):
        task_id = int(call.data.split(":")[1])
        chat_id = call.message.chat.id

        if mark_task_completed(chat_id, task_id):
            bot.answer_callback_query(call.id, "✅ Задача выполнена.")
            send_task_list(bot, chat_id, edit=True, message_id=call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "⚠️ Не удалось обновить задачу.")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("delete:"))
    def handle_delete_task(call):
        task_id = int(call.data.split(":")[1])
        chat_id = call.message.chat.id

        if delete_task(chat_id, str(task_id)):
            bot.answer_callback_query(call.id, "🗑 Задача удалена.")
            send_task_list(bot, chat_id, edit=True, message_id=call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "⚠️ Не удалось удалить задачу.")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("list_tasks"))
    def send_task_list(bot, chat_id, edit=False, message_id=None):
        tasks = get_tasks(chat_id)
        if not tasks:
            if edit:
                bot.edit_message_text("📭 У тебя пока нет задач.", chat_id, message_id)
            else:
                bot.send_message(chat_id, "📭 У тебя пока нет задач.")
            return

        # Формируем таблицу
        headers = ["ID", "Задача", "Создана", "Срок", "Статус"]
        rows = []
        for task_id, task_text, created_at, due_date, is_done in tasks:
            status = "✅" if is_done else "❌"
            created_str = created_at.split(" ")[0] if created_at else "—"
            due_str = due_date if due_date else "—"
            rows.append([task_id, task_text[:30], created_str, due_str, status])

        table_text = tabulate(rows, headers, tablefmt="plain", stralign="center")

        text = "📋 *Твои задачи:*\n```\n" + table_text + "\n```"

        markup = types.InlineKeyboardMarkup()
        for task_id, _, _, _, is_done in tasks:
            row = []
            if not is_done:
                row.append(types.InlineKeyboardButton(callback_data=f"complete:{task_id}", text=f"{task_id} - ✅ Выполнена"))
            row.append(types.InlineKeyboardButton(callback_data=f"delete:{task_id}", text=f"{task_id} - 🗑 Удалить"))
            markup.add(*row)

        if edit:
            bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)
        else:
            bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)
