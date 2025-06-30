from telebot import types
from db.queries import get_state, set_state, add_task
from services.currency import get_currency
from services.quote import get_quote
from ui.ui import get_main_menu
# from handlers.tasks import add_task_start


def register_main_menu_handlers(bot):
    @bot.message_handler(content_types=["text"])
    def text_handler(message):
        chat_id = message.chat.id
        state = get_state(chat_id)

        # 💡 Если ожидается ввод в другом хендлере — не мешаем
        if state in ["awaiting_feedback", "awaiting_weather_city", "awaiting_time"]:
            return

        text = message.text.strip()

        # Поведение при выборе пункта меню
        actions = {
            "🌤 Погода": lambda: (set_state(chat_id, "awaiting_weather_city"),
                                 bot.send_message(chat_id, "Введи город:")),
            "💱 Курс валют": lambda: bot.send_message(chat_id, get_currency(), reply_markup=get_main_menu()),
            "🧠 Мысль дня": lambda: bot.send_message(chat_id, get_quote(), reply_markup=get_main_menu()),
            "📝 Добавить дело": lambda: (
                set_state(chat_id, "awaiting_task_text"),
                bot.send_message(chat_id, "✍️ Введи текст задачи, которую хочешь добавить:",
                                 reply_markup=types.ReplyKeyboardRemove())
            ),

            "⏰ Время рассылки": lambda: (set_state(chat_id, "awaiting_time"),
                                         bot.send_message(chat_id, "Введи время в формате ЧЧ:ММ",
                                                          reply_markup=get_main_menu())),
            "📬 Обратная связь": lambda: (set_state(chat_id, "awaiting_feedback"),
                                         bot.send_message(chat_id,
                                                          "✉ Напиши, что бы ты хотел улучшить в боте. Я обязательно прочитаю!"))
        }
        if text in actions:
            actions[text]()
