import pytest
from datetime import datetime, timedelta
from nlp.parser import parse_intent
from db.queries import add_task, get_tasks
import sqlite3
import os

TEST_DB = "test_tasks.db"

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    # Переопределяем БД на тестовую
    monkeypatch.setattr("db.init_db.DB_PATH", TEST_DB)

    # Создаем пустую БД
    conn = sqlite3.connect(TEST_DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            task TEXT,
            due_date TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

    yield

    # После теста удаляем БД
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_add_task_with_datetime_in_db():
    text = "купить хлеб завтра в 10:30"
    result = parse_intent(text)

    # Проверка парсера
    assert result["intent"] == "add_task"
    assert "купить хлеб" in result["task"]
    assert result["date"] is not None

    expected_date = (datetime.now() + timedelta(days=1)).replace(hour=10, minute=30, second=0, microsecond=0)
    assert result["date"].replace(second=0, microsecond=0) == expected_date

    # Сохраняем в БД
    add_task(chat_id=1, task=result["task"], due_date=result["date"])

    # Читаем из БД
    tasks = get_tasks(1)
    assert len(tasks) == 1

    db_task = tasks[0]
    db_due_date = datetime.fromisoformat(db_task[2])  # due_date в ISO
    assert db_due_date.replace(second=0, microsecond=0) == expected_date
