from feedback import register_feedback_handlers
from quote import register_quote_handlers
from schedule import register_schedule_handlers
from weather import register_weather_handlers
from main_menu import register_main_menu_handlers, get_main_menu


def register_handlers(bot):
    # Сначала регистрируем хэндлеры с передачей get_main_menu, где нужно
    register_feedback_handlers(bot)
    register_quote_handlers(bot, get_main_menu)
    register_schedule_handlers(bot, get_main_menu)
    register_weather_handlers(bot, get_main_menu)
    register_main_menu_handlers(bot)
