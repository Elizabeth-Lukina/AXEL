from services.nlp.parser import parse_intent
from db.queries import add_task, delete_task_by_text
from telebot.types import Message
from services.nlp import parse_intent
from ui.ui import get_menu_tasks


def handle_free_text(bot, message: Message, user_id: int):
    intent, entities = parse_intent(message.text)
    print(f"[DEBUG] Обнаружен интент: {intent}, сущности: {entities}")

    if intent == "unknown":
        bot.send_message(user_id, "🤖 Не понял задачу. Попробуй переформулировать.")
        return

    task_text = message.text
    add_task(user_id, task_text, intent=intent)
    bot.send_message(user_id, f"✅ Добавил задачу с интентом «{intent}»", reply_markup=get_menu_tasks())
