import json
import logging
from pathlib import Path

from expense import Expense


DATA_FILE: Path = Path("expenses.json")
LOG_FILE: Path = Path("app.log")


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

logger = logging.getLogger(__name__)


def load_expenses() -> list[Expense]:
    """Load expenses from JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data: object = json.load(file)

        if not isinstance(data, list):
            logger.error("Invalid JSON structure in expenses file")
            return []

        expenses: list[Expense] = []

        for item in data:
            if not isinstance(item, dict):
                continue

            title = item.get("title")
            amount = item.get("amount")
            category = item.get("category")

            if (
                isinstance(title, str)
                and isinstance(amount, (int, float))
                and isinstance(category, str)
            ):
                expenses.append(
                    Expense(
                        title=title,
                        amount=float(amount),
                        category=category,
                    )
                )

        return expenses

    except (json.JSONDecodeError, OSError) as error:
        logger.error("Failed to load expenses: %s", error)
        return []


def save_expenses(expenses: list[Expense]) -> None:
    """Save expenses to JSON file."""
    data: list[dict[str, str | float]] = [
        expense.to_dict() for expense in expenses
    ]

    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )
    except OSError as error:
        logger.error("Failed to save expenses: %s", error)


def add_expense(expenses: list[Expense]) -> None:
    """Add a new expense."""
    title: str = input("Назва: ").strip()

    if not title:
        print("Назва не може бути порожньою.")
        logger.warning("Empty expense title entered")
        return

    try:
        amount: float = float(
            input("Сума: ").replace(",", ".")
        )

        if amount <= 0:
            raise ValueError

    except ValueError:
        print("Помилка: сума повинна бути додатним числом.")
        logger.warning("Invalid expense amount entered")
        return

    category: str = input("Категорія: ").strip()

    if not category:
        print("Категорія не може бути порожньою.")
        logger.warning("Empty expense category entered")
        return

    expense = Expense(
        title=title,
        amount=amount,
        category=category,
    )

    expenses.append(expense)
    save_expenses(expenses)

    logger.info(
        "Expense added: %s, %.2f, %s",
        title,
        amount,
        category,
    )

    print("Витрату успішно додано.")


def show_expenses(expenses: list[Expense]) -> None:
    """Display all expenses."""
    logger.info("Viewing all expenses")

    if not expenses:
        print("Список витрат порожній.")
        return

    print("\nСписок витрат:")

    for number, expense in enumerate(expenses, start=1):
        print(f"{number}. {expense}")


def show_expenses_by_category(
    expenses: list[Expense],
) -> None:
    """Display expenses filtered by category."""
    category: str = input(
        "Введіть категорію: "
    ).strip()

    filtered_expenses: list[Expense] = [
        expense
        for expense in expenses
        if expense.category.lower() == category.lower()
    ]

    logger.info(
        "Viewing expenses by category: %s",
        category,
    )

    if not filtered_expenses:
        print(
            f'Витрат у категорії "{category}" не знайдено.'
        )
        return

    print(f'\nВитрати категорії "{category}":')

    for number, expense in enumerate(
        filtered_expenses,
        start=1,
    ):
        print(f"{number}. {expense}")


def show_total(expenses: list[Expense]) -> None:
    """Display total expenses amount."""
    total: float = sum(
        expense.amount for expense in expenses
    )

    logger.info(
        "Total expenses calculated: %.2f",
        total,
    )

    print(f"Загальна сума витрат: {total:.2f} грн")


def show_menu() -> None:
    """Display application menu."""
    print("\n=== Менеджер особистих витрат ===")
    print("1. Додати витрату")
    print("2. Показати всі витрати")
    print("3. Показати витрати за категорією")
    print("4. Показати загальну суму")
    print("5. Вийти")


def main() -> None:
    """Run the application."""
    logger.info("Application started")

    expenses: list[Expense] = load_expenses()

    while True:
        show_menu()

        choice: str = input(
            "\nОберіть пункт меню: "
        ).strip()

        match choice:
            case "1":
                add_expense(expenses)

            case "2":
                show_expenses(expenses)

            case "3":
                show_expenses_by_category(expenses)

            case "4":
                show_total(expenses)

            case "5":
                logger.info("Application stopped")
                print("До побачення!")
                break

            case _:
                logger.warning(
                    "Invalid menu option entered: %s",
                    choice,
                )
                print(
                    "Невірний пункт меню. "
                    "Оберіть число від 1 до 5."
                )


if __name__ == "__main__":
    main()