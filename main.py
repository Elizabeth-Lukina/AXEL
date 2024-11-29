# import asyncio
# import logging
import telebot
from config import token

bot = telebot.TeleBot(token)








if __name__ == '__main__':
    bot.polling(none_stop=True)
