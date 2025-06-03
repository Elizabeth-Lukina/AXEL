import requests
from config import CUR_API_KEY


def get_currency():
    try:
        url = "https://api.freecurrencyapi.com/v1/latest"

        # USD к RUB
        response_usd = requests.get(url, params={"apikey": CUR_API_KEY, "base_currency": "USD", "currencies": "RUB"})
        response_usd.raise_for_status()  # Проверка на успешный ответ
        data_usd = response_usd.json()
        usd_rub = data_usd["data"]["RUB"]
        print(f"USD к RUB: {usd_rub}")

        # EUR к RUB
        response_eur = requests.get(url, params={"apikey": CUR_API_KEY, "base_currency": "EUR", "currencies": "RUB"})
        response_eur.raise_for_status()  # Проверка на успешный ответ
        data_eur = response_eur.json()
        eur_rub = data_eur["data"]["RUB"]
        print(f"EUR к RUB: {eur_rub}")

        return f"💵 USD: {usd_rub:.2f} ₽\n💶 EUR: {eur_rub:.2f} ₽"

    except Exception as e:
        return f"Ошибка получения курса валют: {e}"


print(get_currency())