import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def init_db():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS usage_log (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT,
                command TEXT,
                extra TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS users (
                chat_id BIGINT PRIMARY KEY,
                city TEXT DEFAULT 'Санкт-Петербург',
                daily_enabled BOOLEAN DEFAULT TRUE
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT,
                task TEXT,
                due_date DATE,
                done BOOLEAN DEFAULT FALSE
            );
            """)
        conn.commit()


def save_user(chat_id, city):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (chat_id, city)
                VALUES (%s, %s)
                ON CONFLICT (chat_id)
                DO UPDATE SET city = EXCLUDED.city;
            """, (chat_id, city))
        conn.commit()


def user_exists(chat_id):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE chat_id = %s LIMIT 1;", (chat_id,))
            return cur.fetchone() is not None


def set_state(chat_id, state):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET state = %s WHERE chat_id = %s;", (state, chat_id))


def get_state(chat_id):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT state FROM users WHERE chat_id = %s;", (chat_id,))
            result = cur.fetchone()
            return result[0] if result else None


def clear_state(chat_id):
    set_state(chat_id, None)
