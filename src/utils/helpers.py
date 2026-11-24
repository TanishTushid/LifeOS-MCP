from datetime import date, datetime
from typing import Any, Iterable, Literal


TaskPriority = Literal["low", "medium", "high"]
TaskStatus = Literal["pending", "completed"]


def clean_text(value: str | None, default: str = "") -> str:
    """Strip surrounding whitespace and return a default for missing values."""
    if value is None:
        return default

    cleaned = value.strip()
    return cleaned or default


def validate_required_text(value: str | None, field_name: str = "Value") -> str:
    """Return cleaned text or raise a clear error when it is empty."""
    cleaned = clean_text(value)
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def normalize_category(category: str | None) -> str:
    """Normalize an optional note category."""
    return clean_text(category, "general")


def validate_priority(priority: str) -> TaskPriority:
    """Validate and return a task priority."""
    normalized = priority.strip().lower()
    if normalized not in ("low", "medium", "high"):
        raise ValueError("Priority must be low, medium, or high")
    return normalized  # type: ignore[return-value]


def validate_status(status: str) -> TaskStatus:
    """Validate and return a task or reminder status."""
    normalized = status.strip().lower()
    if normalized not in ("pending", "completed"):
        raise ValueError("Status must be pending or completed")
    return normalized  # type: ignore[return-value]


def parse_iso_datetime(value: str) -> datetime:
    """Parse an ISO 8601 date or datetime and return a datetime."""
    try:
        return datetime.fromisoformat(value.strip())
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("Invalid date format. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS") from exc


def parse_due_date(value: str) -> date:
    """Parse a due date in ISO 8601 format."""
    cleaned = clean_text(value)
    if not cleaned:
        raise ValueError("Due date cannot be empty")

    try:
        return date.fromisoformat(cleaned)
    except ValueError as exc:
        raise ValueError("Invalid due date. Use YYYY-MM-DD") from exc


def format_iso_datetime(value: datetime | str) -> str:
    """Format a datetime or ISO datetime string consistently."""
    if isinstance(value, datetime):
        return value.isoformat()
    return parse_iso_datetime(value).isoformat()


def format_due_date(value: date | datetime | str) -> str:
    """Format a date value as YYYY-MM-DD."""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()

    cleaned = clean_text(value)
    if not cleaned:
        return ""
    return parse_due_date(cleaned).isoformat()


def success(message: str, **details: Any) -> dict[str, Any]:
    """Build a standard successful tool response."""
    return {"success": True, "message": message, **details}


def error(message: str, **details: Any) -> dict[str, Any]:
    """Build a standard error tool response."""
    return {"success": False, "message": message, **details}


def calculate_completion_rate(completed: int, total: int) -> float:
    """Calculate a completion percentage, rounded to two decimal places."""
    if total <= 0:
        return 0.0
    if completed < 0:
        raise ValueError("Completed count cannot be negative")
    if completed > total:
        raise ValueError("Completed count cannot exceed total count")
    return round((completed / total) * 100, 2)


def format_rows(rows: Iterable[Any]) -> list[dict[str, Any]]:
    """Convert SQLite rows or mappings to plain dictionaries."""
    formatted: list[dict[str, Any]] = []
    for row in rows:
        if hasattr(row, "keys"):
            formatted.append(dict(row))
        elif isinstance(row, dict):
            formatted.append(row.copy())
        else:
            raise TypeError("Rows must be SQLite Row objects or dictionaries")
    return formatted
