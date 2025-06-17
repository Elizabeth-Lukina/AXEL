import os
import matplotlib.pyplot as plt
import requests
from datetime import date, timedelta
from db.init_db import connect

def get_task_stats(chat_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM tasks WHERE chat_id = ?;", (chat_id,))
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tasks WHERE chat_id = ? AND done = 1;", (chat_id,))
    done = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT due_date), 0) FROM tasks WHERE chat_id = ?;", (chat_id,))
    avg = cur.fetchone()[0] or 0

    cur.execute("SELECT strftime('%w', due_date), COUNT(*) FROM tasks WHERE chat_id = ? GROUP BY 1 ORDER BY 2 DESC LIMIT 1;", (chat_id,))
    max_day = cur.fetchone()

    cur.close()
    conn.close()

    text = f"📊 Задачи всего: {total}\n✅ Выполнено: {done}\n📆 Среднее в день: {avg:.2f}"
    if max_day:
        days = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        text += f"\n📈 Самый загруженный день: {days[int(max_day[0])]} ({max_day[1]} задач)"
    return text
def log_usage(chat_id, command, extra=None):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO usage_log (chat_id, command, extra)
        VALUES (?, ?, ?)
    """, (chat_id, command, extra))
    conn.commit()
    cur.close()
    conn.close()
def get_city_chart():
    os.makedirs("charts", exist_ok=True)
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT extra, COUNT(*) FROM usage_log WHERE command='weather_query' GROUP BY extra ORDER BY COUNT(*) DESC LIMIT 5;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    cities = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    plt.figure(figsize=(8, 5))
    plt.bar(cities, counts, color='skyblue')
    plt.title('🏙 Топ-5 городов по числу запросов')
    plt.xlabel('Город')
    plt.ylabel('Запросы')
    plt.tight_layout()

    chart_path = os.path.join("charts", "top_cities.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def get_stats(chat_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM tasks WHERE chat_id = ?;", (chat_id,))
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tasks WHERE chat_id = ? AND done = 1;", (chat_id,))
    done = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT due_date), 0) FROM tasks WHERE chat_id = ?;", (chat_id,))
    avg = cur.fetchone()[0] or 0

    cur.execute("SELECT strftime('%w', due_date), COUNT(*) FROM tasks WHERE chat_id = ? GROUP BY 1 ORDER BY 2 DESC LIMIT 1;", (chat_id,))
    max_day = cur.fetchone()

    cur.close()
    conn.close()

    text = f"📊 Задачи всего: {total}\n✅ Выполнено: {done}\n📆 Среднее в день: {avg:.2f}"
    if max_day:
        days = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        text += f"\n📈 Самый загруженный день: {days[int(max_day[0])]} ({max_day[1]} задач)"
    return text

def get_currency_history_chart():
    os.makedirs("charts", exist_ok=True)
    end_date = date.today()
    start_date = end_date - timedelta(days=6)
    dates = []
    usd_rates = []
    eur_rates = []
    for i in range(7):
        d = start_date + timedelta(days=i)
        d_str = d.strftime("%Y-%m-%d")
        resp_usd = requests.get(f"https://api.exchangerate.host/{d_str}", params={"base": "USD", "symbols": "RUB"})
        data_usd = resp_usd.json()
        usd_rates.append(data_usd["rates"]["RUB"])
        resp_eur = requests.get(f"https://api.exchangerate.host/{d_str}", params={"base": "EUR", "symbols": "RUB"})
        data_eur = resp_eur.json()
        eur_rates.append(data_eur["rates"]["RUB"])
        dates.append(d_str)

    plt.figure(figsize=(8, 5))
    plt.plot(dates, usd_rates, label="USD->RUB", marker='o')
    plt.plot(dates, eur_rates, label="EUR->RUB", marker='o')
    plt.title("📈 Курс USD и EUR к RUB за последнюю неделю")
    plt.xlabel("Дата")
    plt.ylabel("Курс")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    chart_path = os.path.join("charts", "currency_history.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path
