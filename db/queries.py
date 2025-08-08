from datetime import datetime
from db.init_db import connect


def save_user(chat_id, city):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (chat_id, city, preferences)
            VALUES (?, ?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET city = excluded.city;
        """, (chat_id, city, ""))
        conn.commit()


def user_exists(chat_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE chat_id = ? LIMIT 1;", (chat_id,))
        return cur.fetchone() is not None


def set_state(chat_id, state):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE chat_id = ?", (chat_id,))
        exists = cur.fetchone()

        if exists:
            cur.execute("UPDATE users SET state = ? WHERE chat_id = ?", (state, chat_id))
        else:
            cur.execute("INSERT INTO users (chat_id, state) VALUES (?, ?)", (chat_id, state))

        conn.commit()


def get_state(chat_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT state FROM users WHERE chat_id = ?;", (chat_id,))
        result = cur.fetchone()
        print(f"[DEBUG] get_state({chat_id}) = {result}")
        return result[0] if result else None


def update_user_time(chat_id, hour, minute):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET send_hour = ?, send_minute = ? WHERE chat_id = ?;",
            (hour, minute, chat_id)
        )
        conn.commit()


def clear_state(chat_id):
    set_state(chat_id, None)


def save_feedback(chat_id, username, message):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO feedback (chat_id, username, message)
            VALUES (?, ?, ?)
        """, (chat_id, username, message))
        conn.commit()


def add_task(chat_id, task, intent=None, due_date=None):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tasks (chat_id, task, intent, created_at, due_date, is_done)
            VALUES (?, ?, ?, ?, ?, 0)
        """, (
            chat_id,
            task,
            intent,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            due_date.strftime("%Y-%m-%d") if due_date else None
        ))
        conn.commit()


def delete_task(chat_id, text_or_id):
    """Удаляет по id (число) или по фрагменту текста"""
    with connect() as conn:
        cur = conn.cursor()
        if text_or_id.isdigit():
            cur.execute("DELETE FROM tasks WHERE chat_id = ? AND id = ?", (chat_id, int(text_or_id)))
        else:
            cur.execute("DELETE FROM tasks WHERE chat_id = ? AND task LIKE ?", (chat_id, f"%{text_or_id}%"))
        conn.commit()
        return cur.rowcount > 0


def reschedule_task(chat_id, text_or_id, new_date: datetime):
    with connect() as conn:
        cur = conn.cursor()
        if text_or_id.isdigit():
            cur.execute(
                "UPDATE tasks SET due_date = ? WHERE chat_id = ? AND id = ?",
                (new_date.strftime("%Y-%m-%d"), chat_id, int(text_or_id))
            )
        else:
            cur.execute(
                "UPDATE tasks SET due_date = ? WHERE chat_id = ? AND task LIKE ?",
                (new_date.strftime("%Y-%m-%d"), chat_id, f"%{text_or_id}%")
            )
        conn.commit()
        return cur.rowcount > 0


def get_tasks(chat_id):
    """Возвращает все задачи с полями для таблицы"""
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, task, created_at, due_date, is_done
            FROM tasks
            WHERE chat_id = ?
            ORDER BY is_done ASC, due_date ASC NULLS LAST, created_at DESC
        """, (chat_id,))
        return cur.fetchall()


def mark_task_completed(chat_id, task_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET is_done = 1 WHERE chat_id = ? AND id = ?", (chat_id, task_id))
        conn.commit()
        return cur.rowcount > 0


def get_tasks_by_date(chat_id, date: datetime):
    with connect() as conn:
        cur = conn.cursor()
        date_str = date.strftime("%Y-%m-%d")
        cur.execute("""
            SELECT id, task, created_at, due_date, is_done
            FROM tasks
            WHERE chat_id = ? AND date(due_date) = ?
            ORDER BY is_done ASC, due_date ASC
        """, (chat_id, date_str))
        return cur.fetchall()

def complete_task(chat_id: int, text: str) -> bool:
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE tasks SET is_done = 1 WHERE chat_id = ? AND task LIKE ?",
            (chat_id, f"%{text}%")
        )
        conn.commit()
        return cur.rowcount > 0



def save_preferences(chat_id, prefs: list):
    conn = connect()
    c = conn.cursor()
    prefs_str = ",".join(prefs)
    c.execute("UPDATE users SET preferences = ? WHERE chat_id = ?", (prefs_str, chat_id))
    conn.commit()
    conn.close()


def get_preferences(chat_id):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT preferences FROM users WHERE chat_id = ?", (chat_id,))
    row = c.fetchone()
    conn.close()
    if row and row[0]:
        return row[0].split(",")
    return []
