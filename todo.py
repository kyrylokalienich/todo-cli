import argparse
import db


def main():
    db.init_db()

    parser = argparse.ArgumentParser(description="Todo CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Додати задачу")
    add_parser.add_argument("title", help="Назва задачі")

    subparsers.add_parser("list", help="Показати всі задачі")
    
    done_parser = subparsers.add_parser("done", help="Позначити задачу виконаною")
    done_parser.add_argument("task_id", type=int, help="ID задачі")

    status_parser = subparsers.add_parser("update-status", help="Оновити статус задачі")
    status_parser.add_argument("task_id", type=int, help="ID задачі")
    status_parser.add_argument(
        "status",
        type=db.validate_status,
        help="Новий статус задачі (ToDo, InProgress, Done, Hold, Blocked)",
    )

    completion_parser = subparsers.add_parser(
        "update-completion",
        help="Оновити відсоток виконання задачі",
    )
    completion_parser.add_argument("task_id", type=int, help="ID задачі")
    completion_parser.add_argument(
        "percent",
        type=int,
        help="Відсоток завершення (0-100)",
    )

    del_parser = subparsers.add_parser("delete", help="Видалити задачу")
    del_parser.add_argument("task_id", type=int, help="ID задачі")

    search_parser = subparsers.add_parser("search", help="Пошук задач за ключовим словом")
    search_parser.add_argument("keyword", help="Слово для пошуку")

    args = parser.parse_args()

    if args.command == "add":
        db.add_task(args.title)
    elif args.command == "list":
        db.list_tasks()
    elif args.command == "done":
        db.complete_task(args.task_id)
    elif args.command == "update-status":
        db.update_status(args.task_id, args.status)
    elif args.command == "update-completion":
        db.update_completion(args.task_id, args.percent)
    elif args.command == "delete":
        db.delete_task(args.task_id)
    elif args.command == "search":
        db.search_tasks(args.keyword)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
