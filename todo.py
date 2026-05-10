import argparse
import db

def main():
    db.init_db()

    parser = argparse.ArgumentParser(description="Todo CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Додати задачу")
    add_parser.add_argument("title", help="Назва задачі")

    subparsers.add_parser("list", help="Показати всі задачі")

    args = parser.parse_args()

    if args.command == "add":
        db.add_task(args.title)
    elif args.command == "list":
        db.list_tasks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()