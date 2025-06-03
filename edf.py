import sqlite3

conn = sqlite3.connect("weatherbot.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(users);")
columns = cursor.fetchall()

print("Таблица users:")
for col in columns:
    print(col)

conn.close()
