from domain import MalformedTask
from readers.toolkit.scalars import comma_items


def expand_rank(spec: str, named_sets: dict[str, list[int]]) -> list[int]:
    ordinals: list[int] = []
    for token in comma_items(spec):
        if token in named_sets:
            ordinals.extend(named_sets[token])
        else:
            ordinals.extend(_expand_token(token))
    return ordinals


def _expand_token(token: str) -> range | list[int]:
    try:
        bounds = [int(piece) for piece in token.split("-")]
    except ValueError:
        raise MalformedTask(f"Некорректная спецификация номеров тестов: '{token}'")

    if len(bounds) == 1:
        return bounds

    if len(bounds) not in (2, 3):
        raise MalformedTask(f"Некорректная спецификация номеров тестов: '{token}'")

    low, high, *rest = bounds
    stride = rest[0] if rest else 1
    if stride <= 0:
        raise MalformedTask(f"Шаг диапазона должен быть положительным: '{token}'")
    return range(low, high + 1, stride)
