import sqlite3
from db.init_db import connect

def column_exists(cur, table, col):
    cur.execute(f"PRAGMA table_info({table});")
    return any(r[1] == col for r in cur.fetchall())

def run_migration():
    with connect() as conn:
        cur = conn.cursor()

        if not column_exists(cur, "tasks", "created_at"):
            cur.execute("ALTER TABLE tasks ADD COLUMN created_at TEXT;")
        if not column_exists(cur, "tasks", "due_date"):
            cur.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT;")
        if not column_exists(cur, "tasks", "is_done"):
            cur.execute("ALTER TABLE tasks ADD COLUMN is_done INTEGER DEFAULT 0;")
        if not column_exists(cur, "tasks", "notified_24h"):
            cur.execute("ALTER TABLE tasks ADD COLUMN notified_24h INTEGER DEFAULT 0;")
        if not column_exists(cur, "tasks", "notified_1h"):
            cur.execute("ALTER TABLE tasks ADD COLUMN notified_1h INTEGER DEFAULT 0;")

        # заполнить created_at для старых записей (если пусто)
        cur.execute("UPDATE tasks SET created_at = COALESCE(created_at, strftime('%Y-%m-%d %H:%M:%S','now'));")
        conn.commit()
        cur.close()

if __name__ == "__main__":
    run_migration()
    print("Migration finished")