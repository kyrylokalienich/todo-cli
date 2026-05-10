import sqlite3

DB_FILE = "todo.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                title   TEXT    NOT NULL,
                done    INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()

def add_task(title: str):
    with get_connection() as conn:
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
    print(f"✓ Задачу додано: {title}")

def list_tasks():
    with get_connection() as conn:
        rows = conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
    if not rows:
        print("Список порожній.")
        return
    for row in rows:
        status = "✓" if row[2] else "○"
        print(f"  [{row[0]}] {status} {row[1]}")