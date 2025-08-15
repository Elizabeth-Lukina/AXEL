from telebot import types
from db.queries import (
    get_state, set_state, clear_state, save_preferences, get_preferences,
    update_user_time, disable_daily_report
)
from services.daily_report import schedule_report_for_user, scheduler
from ui.ui import get_main_menu, get_subscription_items_keyboard, get_manage_subscription_menu


def register_manage_subscription_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == "⏰ Управление рассылкой")
    def manage_subscription(message):
        chat_id = message.chat.id
        bot.send_message(chat_id, "Что хочешь сделать с рассылкой?",
                         reply_markup=get_manage_subscription_menu())
        set_state(chat_id, "awaiting_manage_choice")

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_manage_choice")
    def handle_manage_choice(message):
        chat_id = message.chat.id
        text = message.text.strip()

        if text == "✏ Изменить содержание":
            bot.send_message(chat_id, "Выбери, что хочешь получать в рассылке:",
                             reply_markup=get_subscription_items_keyboard())
            set_state(chat_id, "awaiting_subscription_items")

        elif text == "⏰ Изменить время":
            bot.send_message(chat_id, "Введи новое время рассылки в формате ЧЧ:ММ")
            set_state(chat_id, "awaiting_time")

        elif text == "🚫 Отменить рассылку":
            disable_daily_report(chat_id)
            try:
                scheduler.remove_job(f"report_{chat_id}")
            except:
                pass
            clear_state(chat_id)
            bot.send_message(chat_id, "❌ Рассылка отключена.",
                             reply_markup=get_main_menu())

        elif text == "⬅ Назад в главное меню":
            clear_state(chat_id)
            bot.send_message(chat_id, "Возвращаемся в главное меню.",
                             reply_markup=get_main_menu())

        else:
            bot.send_message(chat_id, "Выбери действие из кнопок.",
                             reply_markup=get_manage_subscription_menu())
