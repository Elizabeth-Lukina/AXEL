from telebot import types

from services.daily_report import schedule_report_for_user
from db.queries import user_exists, set_state, get_state, save_preferences, get_preferences, update_user_time, \
    clear_state
from ui.ui import get_main_menu, get_subscription_items_keyboard, get_yes_no_keyboard


def register_handlers_start(bot):
    @bot.message_handler(commands=["start"])
    def start(message):
        chat_id = message.chat.id
        username = message.from_user.username or 'неизвестно'
        if not user_exists(chat_id):
            bot.send_message(chat_id, f" ✌ Йоу, йоу, йоу! Привет, {username}!\n"
                                      f"Я твой личный ассистент — AXIOM!\n"
                                      f"Точнее пока только учусь им быть, но постараюсь быть уже полезным.")

            bot.send_message(chat_id, "Хочешь получать утреннюю рассылку?", reply_markup=get_yes_no_keyboard())
            set_state(chat_id, "awaiting_subscription_choice")
        else:
            bot.send_message(chat_id, "Мы же уже знакомы, чем займемся?", reply_markup=get_main_menu())

    @bot.message_handler(func=lambda message: get_state(message.chat.id) == "awaiting_subscription_choice")
    def handle_subscription_choice(message):
        chat_id = message.chat.id
        text = message.text.strip()

        if text == "✅ Да":
            bot.send_message(chat_id, "Выбери, что хочешь получать в рассылке:",
                             reply_markup=get_subscription_items_keyboard())
            set_state(chat_id, "awaiting_subscription_items")

        elif text == "❌ Нет":
            save_preferences(chat_id, [])
            bot.send_message(chat_id, "Понял, значит не хочешь.", reply_markup=types.ReplyKeyboardRemove())
            clear_state(chat_id)
            bot.send_message(chat_id, "Тогда, чем займемся?", reply_markup=get_main_menu())

        else:
            bot.send_message(chat_id, "Пожалуйста, выбери «✅ Да» или «❌ Нет».")

    @bot.message_handler(func=lambda message: get_state(message.chat.id) == "awaiting_subscription_items")
    def handle_subscription_items(message):
        chat_id = message.chat.id
        text = message.text.strip()

        # Обновлённый список с иконками
        valid_items = {
            "🌤 Погода": "Погода",
            "💱 Курс валют": "Курс валют",
            "🧠 Мысль дня": "Мысль дня"
        }

        prefs = get_preferences(chat_id) or []

        if text == "✅ Готово":
            if not prefs:
                bot.send_message(chat_id, "Ты не выбрал ни одного пункта. Попробуй ещё раз.",
                                 reply_markup=get_subscription_items_keyboard())
                return

            bot.send_message(chat_id, f"Отлично! Ты выбрал: {', '.join(prefs)}.",
                             reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(chat_id, "Когда хочешь получать рассылку? Введи время в формате ЧЧ:ММ")
            set_state(chat_id, "awaiting_time_start")
            return

        if text in valid_items:
            value = valid_items[text]

            if value not in prefs:
                prefs.append(value)
                save_preferences(chat_id, prefs)

            if value == "Погода":
                bot.send_message(chat_id, "🌦 Для прогноза погоды укажи свой город:")
                set_state(chat_id, "awaiting_city")
                return

            bot.send_message(chat_id, f"Добавлено: {value}. Выбирай дальше или нажми «✅ Готово»",
                             reply_markup=get_subscription_items_keyboard())
        else:
            bot.send_message(chat_id, "Пожалуйста, выбери пункт из кнопок или нажми «✅ Готово»",
                             reply_markup=get_subscription_items_keyboard())

    @bot.message_handler(func=lambda m: get_state(m.chat.id) == "awaiting_time_start")
    def save_send_time(message):
        chat_id = message.chat.id
        try:
            time_str = message.text.strip()
            hour, minute = map(int, time_str.split(":"))

            if 0 <= hour < 24 and 0 <= minute < 60:
                update_user_time(chat_id, hour, minute)
                prefs = get_preferences(chat_id) or []
                clear_state(chat_id)
                schedule_report_for_user(bot, chat_id)

                prefs_str = ", ".join(prefs)
                bot.send_message(chat_id,
                                 f"🎉 Подписка оформлена!\n\n"
                                 f"Ты будешь получать: {prefs_str}.\n"
                                 f"🕒 Каждый день в {hour:02}:{minute:02}.",
                                 reply_markup=get_main_menu())
            else:
                raise ValueError
        except ValueError:
            bot.send_message(chat_id,
                             "Неверный формат времени. Попробуй снова, например 07:30",
                             reply_markup=get_main_menu())
