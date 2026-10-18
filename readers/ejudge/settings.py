import re

from domain import MalformedTask


TARGET_SECTION = "problem"
KEY_SHAPE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def read_problem_section(text: str, label: str) -> dict[str, str]:
    settings: dict[str, str] = {}
    current = None

    for row, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith(("#", ";")):
            continue

        if line.startswith("["):
            if not line.endswith("]"):
                raise MalformedTask(f"{label}, строка {row}: незакрытая секция '{line}'")
            current = line[1:-1].strip()
            continue

        if current != TARGET_SECTION:
            continue

        key, has_value, value = line.partition("=")
        key = key.strip()
        if not KEY_SHAPE.fullmatch(key):
            raise MalformedTask(f"{label}, строка {row}: некорректная строка '{line}'")

        settings[key] = strip_quotes(value.strip()) if has_value else "1"

    if current is None:
        raise MalformedTask(f"В {label} нет секции [problem]")
    return settings


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"')
    return value
