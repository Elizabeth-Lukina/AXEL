import sqlite3
from db.init_db import connect

def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [row[1] for row in cursor.fetchall()]
    return column_name in columns

def run_migration():
    with connect() as conn:
        cur = conn.cursor()

        # created_at
        if not column_exists(cur, "tasks", "created_at"):
            cur.execute("ALTER TABLE tasks ADD COLUMN created_at TEXT;")

        # due_date
        if not column_exists(cur, "tasks", "due_date"):
            cur.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT;")

        # is_done
        if not column_exists(cur, "tasks", "is_done"):
            cur.execute("ALTER TABLE tasks ADD COLUMN is_done INTEGER DEFAULT 0;")

        conn.commit()

if __name__ == "__main__":
    run_migration()
