import enum
import sqlite3

DB_FILE = "todo.db"

class TaskStatus(enum.Enum):
    ToDo = "ToDo"
    InProgress = "InProgress"
    Done = "Done"
    Hold = "Hold"
    Blocked = "Blocked"

    @classmethod
    def names(cls):
        return [member.value for member in cls]


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                title              TEXT    NOT NULL,
                status             TEXT    NOT NULL DEFAULT 'ToDo',
                completion_percent INTEGER NOT NULL DEFAULT 0
            )
        """)
        existing_columns = [row[1] for row in conn.execute("PRAGMA table_info(tasks)").fetchall()]
        if "status" not in existing_columns:
            conn.execute("ALTER TABLE tasks ADD COLUMN status TEXT NOT NULL DEFAULT 'ToDo'")
        if "completion_percent" not in existing_columns:
            conn.execute("ALTER TABLE tasks ADD COLUMN completion_percent INTEGER NOT NULL DEFAULT 0")
        conn.commit()


def validate_status(status: str) -> str:
    normalized = status.strip()
    for allowed in TaskStatus.names():
        if normalized.lower() == allowed.lower():
            return allowed
    raise ValueError(
        f"Невідомий статус: {status}. Доступні статуси: {', '.join(TaskStatus.names())}"
    )


def format_task_row(row):
    return f"  [{row[0]}] {row[2]} {row[3]}% {row[1]}"


def add_task(title: str):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,),
        )
        conn.commit()
    print(f"✓ Задачу додано: {title}")


def list_tasks():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, status, completion_percent FROM tasks ORDER BY id"
        ).fetchall()
    if not rows:
        print("Список порожній.")
        return
    for row in rows:
        print(format_task_row(row))


def complete_task(task_id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE tasks SET status = ?, completion_percent = 100 WHERE id = ?",
            (TaskStatus.Done.value, task_id),
        )
        conn.commit()
    if cursor.rowcount:
        print(f"✓ Задачу #{task_id} позначено як виконану.")
    else:
        print(f"Задачу #{task_id} не знайдено.")


def delete_task(task_id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )
        conn.commit()
    if cursor.rowcount:
        print(f"✓ Задачу #{task_id} видалено.")
    else:
        print(f"Задачу #{task_id} не знайдено.")


def search_tasks(keyword: str):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, status, completion_percent FROM tasks WHERE title LIKE ? ORDER BY id",
            (f"%{keyword}%",),
        ).fetchall()
    if not rows:
        print(f'Нічого не знайдено за запитом: "{keyword}"')
        return
    for row in rows:
        print(format_task_row(row))


def update_status(task_id: int, status: str):
    status_value = validate_status(status)
    with get_connection() as conn:
        if status_value == TaskStatus.Done.value:
            cursor = conn.execute(
                "UPDATE tasks SET status = ?, completion_percent = 100 WHERE id = ?",
                (status_value, task_id),
            )
        else:
            cursor = conn.execute(
                "UPDATE tasks SET status = ? WHERE id = ?",
                (status_value, task_id),
            )
        conn.commit()
    if cursor.rowcount:
        print(f"✓ Статус задачі #{task_id} змінено на {status_value}.")
    else:
        print(f"Задачу #{task_id} не знайдено.")


def update_completion(task_id: int, percent: int):
    if percent < 0 or percent > 100:
        print("Відсоток завершення має бути в діапазоні від 0 до 100.")
        return

    with get_connection() as conn:
        current = conn.execute(
            "SELECT status FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
        if current is None:
            print(f"Задачу #{task_id} не знайдено.")
            return

        current_status = current[0]
        if percent == 100:
            cursor = conn.execute(
                "UPDATE tasks SET completion_percent = ?, status = ? WHERE id = ?",
                (percent, TaskStatus.Done.value, task_id),
            )
        elif current_status == TaskStatus.Done.value:
            cursor = conn.execute(
                "UPDATE tasks SET completion_percent = ?, status = ? WHERE id = ?",
                (percent, TaskStatus.InProgress.value, task_id),
            )
        else:
            cursor = conn.execute(
                "UPDATE tasks SET completion_percent = ? WHERE id = ?",
                (percent, task_id),
            )
        conn.commit()

    if cursor.rowcount:
        print(f"✓ Відсоток завершення задачі #{task_id} оновлено до {percent}%.")
        if percent == 100:
            print(f"✓ Статус задачі #{task_id} автоматично встановлено як {TaskStatus.Done.value}.")
    else:
        print(f"Задачу #{task_id} не знайдено.")
