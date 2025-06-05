import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "weatherbot.db")


def connect():
    return sqlite3.connect(DB_PATH)



def init_db():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usage_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                command TEXT,
                extra TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER PRIMARY KEY,
                city TEXT DEFAULT 'Санкт-Петербург',
                state TEXT,
                daily_enabled BOOLEAN DEFAULT 1,
                send_hour INTEGER DEFAULT 7,
                send_minute INTEGER DEFAULT 30
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                task TEXT,
                due_date DATE,
                done BOOLEAN DEFAULT 0
            );
        """)
        conn.commit()
        cur.close()


def save_user(chat_id, city):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (chat_id, city)
            VALUES (?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET city = excluded.city;
        """, (chat_id, city))
        conn.commit()
        cur.close()


def user_exists(chat_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE chat_id = ? LIMIT 1;",
                    (chat_id,))
        result = cur.fetchone()
        cur.close()
        return result is not None


def set_state(chat_id, state):
    with connect() as conn:
        cur = conn.cursor()

        # Убедиться, что пользователь существует
        cur.execute("SELECT 1 FROM users WHERE chat_id = ?",
                    (chat_id,))
        exists = cur.fetchone()

        if exists:
            cur.execute("UPDATE users SET state = ? WHERE chat_id = ?",
                        (state, chat_id))
        else:
            # Если пользователя нет — создаем
            cur.execute("INSERT INTO users (chat_id, state) VALUES (?, ?)",
                        (chat_id, state))

        conn.commit()


def get_state(chat_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT state FROM users WHERE chat_id = ?;",
                    (chat_id,))
        result = cur.fetchone()
        print(f"[DEBUG] get_state({chat_id}) = {result}")
        cur.close()
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
