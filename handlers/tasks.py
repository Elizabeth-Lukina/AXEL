from db.queries import (
    add_task, delete_task, reschedule_task,
    get_tasks, get_tasks_by_date, mark_done
)
from db.queries import set_state, get_state, clear_state


def register_task_handlers(bot, parse_intent):
    @bot.message_handler(func=lambda m: m.text == "📋 Мои задачи")
    def enter_task_mode(message):
        chat_id = message.chat.id
        set_state(chat_id, "awaiting_task_text")
        bot.send_message(chat_id, "📝 Введи задачу (например: «добавь задачу купить хлеб завтра»):")

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
                msg = f"❌ Удалена: «{task_text}»" if success else "⚠️ Задача не найдена."
                bot.send_message(chat_id, msg)

            elif intent == "reschedule_task":
                success = reschedule_task(chat_id, task_text, date)
                msg = f"🔁 Перенесена на {date.date()}" if success else "⚠️ Не удалось перенести задачу."
                bot.send_message(chat_id, msg)

            elif intent == "list_tasks":
                rows = get_tasks(chat_id)
                clear_state(chat_id)

                if rows:
                    header = "📋 Твои задачи:\n\n"
                    table = "ID | Задача | Создана | Срок | Статус\n"
                    table += "-" * 45 + "\n"
                    for row in rows:
                        id, task, created_at, due_date, is_done = row
                        status = "✅" if is_done else "❌"
                        due = due_date if due_date else "—"
                        table += f"{id} | {task} | {created_at[:10]} | {due} | {status}\n"
                    bot.send_message(chat_id, header + f"```\n{table}```", parse_mode="Markdown")
                else:
                    bot.send_message(chat_id, "📭 У тебя пока нет задач.")

            elif intent == "mark_done":
                task_id = int(result.get("task", "").strip())
                success = mark_done(chat_id, task_id)
                msg = f"✅ Задача {task_id} отмечена как выполненная" if success else "⚠️ Не удалось отметить задачу."
                bot.send_message(chat_id, msg)


            else:
                bot.send_message(chat_id, "🤔 Не понял команду. Попробуй снова.")

            clear_state(chat_id)

        except Exception as e:
            print(f"[ERROR] {e}")
            bot.send_message(chat_id, "⚠️ Ошибка при обработке команды.")
