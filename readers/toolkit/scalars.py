from domain import MalformedTask


def whole_number(raw: str | None, label: str) -> int | None:
    if raw is None or not raw.strip():
        return None
    try:
        return int(raw.strip())
    except ValueError:
        raise MalformedTask(f"{label}: ожидалось целое число, получено '{raw}'")


def real_number(raw: str | None, label: str) -> float | None:
    if raw is None or not raw.strip():
        return None
    try:
        return float(raw.strip())
    except ValueError:
        raise MalformedTask(f"{label}: ожидалось число, получено '{raw}'")


def comma_items(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [piece.strip() for piece in raw.split(",") if piece.strip()]


def seconds_to_ms(seconds: float | None) -> int | None:
    return round(seconds * 1000) if seconds is not None else None
