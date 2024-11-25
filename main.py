import requests
# import telebot
# from telebot import types

# token = token
bot = telebot.TeleBot(token)


# Приветствие от бота
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет ✌ Я - Ботик! Погоду в каком городе ты хочешь узнать? ")
    bot.send_animation(message.chat.id, r'https://usagif.com/wp-content/uploads/2021/01/dobro-pozhlovat-m.gif')





# Функционал
@bot.message_handler(content_types=['text'])
def messages(message):
    if message.text.lower() not in ['спасибо', 'спс', 'рахмет']:
        weather_now(message)
    elif message.text.lower() in ['привет','здравствуй','приветик']:
        hello(message)
    else:
        thanks(message)

def hello(message):
        bot.send_message(message.chat.id, 'Привет, привет мой друг! Выбирай город')


def thanks(message):
    bot.send_message(message.chat.id, 'Всегда рад помочь, заходи еще!')


def weather_now(message):
    api_key = 'c6d194ae86bc7f1338065f24672080c9'
    city = message.text
    try:
        res = requests.get('https://api.openweathermap.org/data/2.5/weather?', params={
            'q': city, 'units': 'metric', 'APPID': api_key, 'lang': 'ru'})
        data = res.json()
        description = data['weather'][0]['description']
        if description == 'облачно с прояснениями':
            bot.send_animation(message.chat.id,
                               r'https://static.life.ru/posts/2019/11/1254455/d7f3798f45c62354415c8f5cea84a748.gif')

        elif description == 'небольшой дождь':
            bot.send_animation(message.chat.id, r'https://99px.ru/sstorage/86/2016/05/image_861905161757111992548.gif')

        elif description == 'ясно':
            bot.send_animation(message.chat.id, r'https://i.gifer.com/1d.gif')

        elif description == 'пасмурно':
            bot.send_animation(message.chat.id, r'https://i.gifer.com/7RtV.gif')

        elif description == 'дождь':
            bot.send_animation(message.chat.id,
                               r'https://media.tenor.com/0uAiSZzuw9gAAAAC/%D0%BB%D0%B5%D1%81-%D0%B4%D0%BE%D0%B6%D0%B4%D1%8C.gif')

        elif description == 'небольшая облачность' or description == 'переменная облачность':
            bot.send_animation(message.chat.id, r'https://i.imgur.com/inO6nq3.gif')

        elif description == 'небольшой снег' or description == 'снег' or description == 'снегопад':
            bot.send_animation(message.chat.id,
                               r'https://i.gifer.com/origin/8b/8bc90224cff030977a722e36e6e736f3_w200.gif')

        bot.reply_to(message, f"Сейчас в городе {city} {data['weather'][0]['description']}, \n"
                              f"Температура воздуха {round(data['main']['temp'], 1)} 0С, \n"
                              f"Влажность {data['main']['humidity']} %, \n"
                              f"Облачность {data['clouds']['all']} % \n"
                              f"Скорость ветра {data['wind']['speed']} м/с")
    except KeyError:
        bot.send_message(message.chat.id, 'Я не знаю такого города, может попробуешь еще раз?)')



if __name__ == '__main__':
    bot.polling(none_stop=True)
