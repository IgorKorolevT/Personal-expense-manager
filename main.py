import logging
from pathlib import Path


DATA_FILE: Path = Path("expenses.json")
LOG_FILE: Path = Path("app.log")


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the application."""
    pass


if __name__ == "__main__":
    main()