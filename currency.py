import requests

def get_currency():
    try:
        url = "https://api.exchangerate.host/latest"

        # USD к RUB
        response_usd = requests.get(url, params={"base": "USD", "symbols": "RUB"})
        data_usd = response_usd.json()
        usd_rub = data_usd["rates"]["RUB"]

        # EUR к RUB
        response_eur = requests.get(url, params={"base": "EUR", "symbols": "RUB"})
        data_eur = response_eur.json()
        eur_rub = data_eur["rates"]["RUB"]

        return f"💵 USD: {usd_rub:.2f} ₽\n💶 EUR: {eur_rub:.2f} ₽"

    except Exception as e:
        return f"Ошибка получения курса валют: {e}"
