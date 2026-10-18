from domain import UnsupportedDialect
from readers.contract import TaskReader


class ReaderCatalog:

    def __init__(self):
        self._by_dialect: dict[str, TaskReader] = {}

    def enroll(self, reader: TaskReader) -> None:
        self._by_dialect[reader.dialect.upper()] = reader

    def pick(self, dialect: str) -> TaskReader:
        reader = self._by_dialect.get(dialect.upper())
        if reader is None:
            raise UnsupportedDialect(
                f"Неизвестный формат '{dialect}'. "
                f"Поддерживаются: {', '.join(self.dialects())}"
            )
        return reader

    def dialects(self) -> list[str]:
        return sorted(self._by_dialect)
