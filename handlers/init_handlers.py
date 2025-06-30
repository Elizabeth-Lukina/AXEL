from handlers.feedback import register_feedback_handlers
from handlers.quote import register_quote_handlers
from handlers.schedule import register_schedule_handlers
from handlers.tasks import register_task_handlers
from handlers.weather import register_weather_handlers
from handlers.main_menu import register_main_menu_handlers, get_main_menu


def register_handlers(bot):
    register_feedback_handlers(bot)
    register_quote_handlers(bot, get_main_menu)
    register_schedule_handlers(bot, get_main_menu)
    register_weather_handlers(bot, get_main_menu)

    register_task_handlers(bot)
    register_main_menu_handlers(bot)
