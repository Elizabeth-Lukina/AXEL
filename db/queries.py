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


def add_task(chat_id, task, intent=None):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (chat_id, task, intent) VALUES (?, ?, ?)",
            (chat_id, task, intent)
        )
        conn.commit()


def get_tasks(chat_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT task FROM tasks WHERE chat_id = ?", (chat_id,))
        return [row[0] for row in cur.fetchall()]


def delete_task_by_text(chat_id: int, text: str) -> bool:
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM tasks WHERE chat_id = ? AND task LIKE ?",
            (chat_id, f"%{text}%")
        )
        conn.commit()
        return cur.rowcount > 0


def reschedule_task_by_text(chat_id: int, text: str, new_date: datetime) -> bool:
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE tasks SET due_date = ? WHERE chat_id = ? AND task LIKE ?",
            (new_date.date(), chat_id, f"%{text}%")
        )
        conn.commit()
        return cur.rowcount > 0


def get_tasks_by_date(chat_id: int, date: datetime):
    with connect() as conn:
        cur = conn.cursor()
        date_str = date.date().isoformat()
        cur.execute(
            "SELECT rowid, task, due_date FROM tasks WHERE chat_id = ? AND date(due_date) = ? ORDER BY due_date ASC",
            (chat_id, date_str)
        )
        rows = cur.fetchall()
        return [{"id": row[0], "task": row[1], "due_date": row[2]} for row in rows]


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
