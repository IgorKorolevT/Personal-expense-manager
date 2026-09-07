class Expense:
    """Represents a single expense."""

    def __init__(self, title: str, amount: float, category: str) -> None:
        self.title: str = title
        self.amount: float = amount
        self.category: str = category

    def __str__(self) -> str:
        return f"{self.title} - {self.amount:.2f} грн - {self.category}"
    