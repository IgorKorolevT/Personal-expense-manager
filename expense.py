class Expense:
    """Represents a single expense."""

    def __init__(self, title: str, amount: float, category: str) -> None:
        self.title: str = title
        self.amount: float = amount
        self.category: str = category

    def to_dict(self) -> dict[str, str | float]:
        """Convert expense to dictionary."""
        return {
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | float]) -> "Expense":
        """Create Expense object from dictionary."""
        return cls(
            title=str(data["title"]),
            amount=float(data["amount"]),
            category=str(data["category"]),
        )

    def __str__(self) -> str:
        return f"{self.title} - {self.amount:.2f} грн - {self.category}"