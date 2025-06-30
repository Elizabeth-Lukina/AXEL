from db.init_db import connect


def save_user(chat_id, city):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (chat_id, city, preferences)
            VALUES (?, ?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET city = excluded.city;
        """, (chat_id, city, ""))  # здесь "" — пустая строка для preferences
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


def save_feedback(chat_id, username, message):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO feedback (chat_id, username, message)
            VALUES (?, ?, ?)
        """, (chat_id, username, message))
        conn.commit()


def add_task(chat_id, task):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (chat_id, task) VALUES (?, ?)", (chat_id, task))
        conn.commit()


def get_tasks(chat_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT task FROM tasks WHERE chat_id = ?", (chat_id,))
        return [row[0] for row in cur.fetchall()]



def save_preferences(chat_id, prefs: list):
    conn = connect()
    c = conn.cursor()
    prefs_str = ",".join(prefs)  # или json.dumps(prefs) для гибкости
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
        return row[0].split(",")  # или json.loads если сохраняешь JSON
    return []
