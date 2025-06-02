import requests
from config import OWM_API_KEY

def get_weather(city):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": OWM_API_KEY,
            "units": "metric",
            "lang": "ru"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("cod") != 200:
            return f"Город '{city}' не найден. Попробуйте снова."

        weather_desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (f"🌤 Погода в {city}:\n"
                f"📌 {weather_desc}\n"
                f"🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n"
                f"💧 Влажность: {humidity}%\n"
                f"💨 Ветер: {wind_speed} м/с")
    except Exception as e:
        return f"Ошибка при получении погоды: {str(e)}"
