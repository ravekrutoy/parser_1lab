import re

from domain import MalformedTask


class SizeNotation:

    def __init__(self, suffixes: dict[str, int], bare_factor: int):
        self._suffixes = {letter.upper(): factor for letter, factor in suffixes.items()}
        self._bare_factor = bare_factor
        letters = "".join(self._suffixes)
        self._shape = re.compile(rf"\s*(\d+)\s*([{letters}]?)\s*", re.IGNORECASE)

    def to_bytes(self, raw: str | None, label: str) -> int | None:
        if raw is None or not raw.strip():
            return None

        found = self._shape.fullmatch(raw)
        if found is None:
            raise MalformedTask(f"{label}: некорректный размер памяти '{raw}'")

        amount, letter = found.groups()
        factor = self._suffixes[letter.upper()] if letter else self._bare_factor
        return int(amount) * factor


KIB = 1024
MIB = 1024 ** 2
GIB = 1024 ** 3
