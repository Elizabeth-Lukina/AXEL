# import psycopg2
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import requests
import os
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


# def connect():
#     return psycopg2.connect(
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         host=DB_HOST,
#         port=DB_PORT
#     )


def log_usage(chat_id, command, extra=None):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO usage_log (chat_id, command, extra) VALUES (%s, %s, %s);",
                (chat_id, command, extra)
            )
        conn.commit()


def get_task_stats(chat_id):  # статистика задач пользователя
    with connect() as conn:
        with conn.cursor() as cur:
            # Всего задач
            cur.execute("SELECT COUNT(*) FROM tasks WHERE chat_id = %s;", (chat_id,))
            total = cur.fetchone()[0]

            # Выполненные задачи
            cur.execute("SELECT COUNT(*) FROM tasks WHERE chat_id = %s AND done = TRUE;", (chat_id,))
            done = cur.fetchone()[0]

            # Среднее в день
            cur.execute(
                "SELECT COUNT(*)::float / NULLIF(COUNT(DISTINCT due_date), 0) FROM tasks WHERE chat_id = %s;",
                (chat_id,)
            )
            avg = cur.fetchone()[0] or 0

            # День недели с наибольшим количеством задач
            cur.execute(
                "SELECT TO_CHAR(due_date, 'Day'), COUNT(*) FROM tasks WHERE chat_id = %s GROUP BY 1 ORDER BY 2 DESC LIMIT 1;",
                (chat_id,)
            )
            max_day = cur.fetchone()

    text = f"📊 Задачи всего: {total}\\n✅ Выполнено: {done}\\n📆 Среднее в день: {avg:.2f}"
    if max_day:
        text += f"\\n📈 Самый загруженный день: {max_day[0].strip()} ({max_day[1]} задач)"
    return text


def get_city_chart():  # построение топ-5 городов
    os.makedirs("../charts", exist_ok=True)
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT extra, COUNT(*) FROM usage_log WHERE command='weather_query' GROUP BY extra ORDER BY COUNT(*) DESC LIMIT 5;")
            rows = cur.fetchall()

    cities = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    plt.figure(figsize=(8, 5))
    plt.bar(cities, counts, color='skyblue')
    plt.title('🏙 Топ-5 городов по числу запросов')
    plt.xlabel('Город')
    plt.ylabel('Запросы')
    plt.tight_layout()

    chart_path = os.path.join("../charts", "top_cities.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path


def get_stats(chat_id):  # аналитика по боту
    with connect() as conn:
        with conn.cursor() as cur:
            # Всего задач
            cur.execute("SELECT COUNT(*) FROM tasks WHERE chat_id = %s;", (chat_id,))
            total = cur.fetchone()[0]

            # Выполненные задачи
            cur.execute("SELECT COUNT(*) FROM tasks WHERE chat_id = %s AND done = TRUE;", (chat_id,))
            done = cur.fetchone()[0]

            # Среднее в день
            cur.execute(
                "SELECT COUNT(*)::float / NULLIF(COUNT(DISTINCT due_date), 0) FROM tasks WHERE chat_id = %s;",
                (chat_id,)
            )
            avg = cur.fetchone()[0] or 0

            # День недели с наибольшим количеством задач
            cur.execute(
                "SELECT TO_CHAR(due_date, 'Day'), COUNT(*) FROM tasks WHERE chat_id = %s GROUP BY 1 ORDER BY 2 DESC LIMIT 1;",
                (chat_id,)
            )
            max_day = cur.fetchone()

    text = f"📊 Задачи всего: {total}\n✅ Выполнено: {done}\n📆 Среднее в день: {avg:.2f}"
    if max_day:
        text += f"\n📈 Самый загруженный день: {max_day[0].strip()} ({max_day[1]} задач)"
    return text


def get_currency_history_chart():  # график курса USD/EUR
    os.makedirs("../charts", exist_ok=True)
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
    chart_path = os.path.join("../charts", "currency_history.png")
    plt.savefig(chart_path)
    plt.close()
    return chart_path
