import traceback
import requests
from config import OPENAI_API_KEY

def ai_reply(prompt):
    try:
        url = "https://api.proxyapi.ru/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 300
        }

        response = requests.post(url, json=payload, headers=headers)

        # Отладка: вывод статуса и текста
        print(f"[AI DEBUG] Status: {response.status_code}")
        print(f"[AI DEBUG] Body: {response.text}")

        data = response.json()

        # Проверяем структуру ответа
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"].strip()
        elif "error" in data:
            return f"❌ Ошибка AI: {data['error'].get('message', 'неизвестная ошибка')}"
        else:
            return "❌ Непредвиденный ответ от AI-сервиса."

    except Exception as e:
        print("[AI ERROR]", traceback.format_exc())
        return f"❌ Ошибка AI: {e}"
