import sqlite3
import os

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Абсолютный путь к папке db
DB_PATH = os.path.join(BASE_DIR, "weatherbot.db")


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
                preferences TEXT,
                city TEXT DEFAULT 'Санкт-Петербург',
                state TEXT,
                daily_enabled BOOLEAN DEFAULT 1,
                send_hour INTEGER DEFAULT 7,
                send_minute INTEGER DEFAULT 30
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                username TEXT,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                task TEXT NOT NULL,
                due_date DATE DEFAULT CURRENT_DATE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        cur.close()
