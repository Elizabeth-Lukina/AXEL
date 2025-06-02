import requests
import psycopg2
from datetime import date
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, TELEGRAM_TOKEN
import telebot

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def get_weather(city):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": "<OPENWEATHERMAP_API_KEY>",
            "units": "metric",
            "lang": "ru"
        }
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("cod") != 200:
            return f"Погода: '{city}' не найден."
        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        return f"☀️ Погода в {city}: {desc}, {temp}°C"
    except:
        return "Погода: ошибка"


def get_rates():
    try:
        response = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=RUB,EUR")
        data = response.json()
        usd_rub = data["rates"]["RUB"]
        eur_rub = data["rates"]["EUR"]
        return f"💱 Курс валют: USD → ₽{usd_rub: .2f} EUR → ₽{eur_rub: .2f}"
    except:
        return "Валюты: ошибка"


def get_tasks(chat_id):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT task FROM tasks WHERE chat_id=%s AND due_date=%s", (chat_id, date.today()))
            tasks = cur.fetchall()
    if not tasks:
        return "✅ На сегодня задач нет."
    task_list = "\n".join(f"— {task[0]}" for task in tasks)
    return f"📋 Задачи на сегодня:\n{task_list}"


def get_quote():
    try:
        r = requests.get("https://zenquotes.io/api/random")
        data = r.json()
        return f"🧠 Мысль дня: {data[0]['q']} — {data[0]['a']}"
    except:
        return "Мысль дня: ошибка"


def send_daily_reports():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT chat_id, city FROM users WHERE daily_enabled = TRUE")
            users = cur.fetchall()

    for chat_id, city in users:
        parts = [
            get_weather(city),
            get_rates(),
            get_tasks(chat_id),
            get_quote()
        ]
        message = "\n\n".join(parts)
        try:
            bot.send_message(chat_id, message)
        except Exception as e:
            print(f"Ошибка отправки для {chat_id}: {e}")
