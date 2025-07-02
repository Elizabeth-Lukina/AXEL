from telebot import types
from db.queries import get_state, update_user_time, clear_state
from services.daily_report import schedule_reports


def register_schedule_handlers(bot, get_main_menu):
    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_time")
    def save_send_time(message):
        try:
            time_str = message.text.strip()
            hour, minute = map(int, time_str.split(":"))

            if 0 <= hour < 24 and 0 <= minute < 60:
                update_user_time(message.chat.id, hour, minute)
                clear_state(message.chat.id)

                schedule_reports(bot)  # передаём именно объект бота

                bot.send_message(message.chat.id, f"Готово! Сводка теперь будет приходить в {hour:02}:{minute:02}.",
                                 reply_markup=get_main_menu())
            else:
                raise ValueError
        except:
            bot.send_message(message.chat.id, "Неверный формат времени. Попробуй снова, например 07:30",
                             reply_markup=get_main_menu())
