from logging import DEBUG

import requests
from bs4 import BeautifulSoup
from random import choice

url = "https://singularity-app.ru/blog/motiviruyushchie-tsitaty/"

def get_quote():
    try:
        data = []
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешный запрос
        # Парсим содержимое страницы
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все блоки с цитатами
        quotes = soup.find_all('blockquote')

        # Извлекаем текст цитат
        for quote in quotes:
            data.append(quote.get_text(strip=True))

        if data:  # Проверяем, есть ли хотя бы одна цитата
            return f"🧠 Мысль дня:\n{choice(data)}"
        else:
            return "Цитаты не найдены"
    except requests.RequestException as e:
        return f"Мысль дня: ошибка при запросе - {e}"
    except Exception as e:
        return f"Мысль дня: ошибка - {e}"


print("[DEBUG]", get_quote())