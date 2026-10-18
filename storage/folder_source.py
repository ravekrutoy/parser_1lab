from pathlib import Path

from domain import SourceUnavailable
from storage.hygiene import is_service_file
from storage.source import FileSource


class FolderFileSource(FileSource):

    def __init__(self, folder: str):
        self._base = Path(folder)
        if not self._base.is_dir():
            raise SourceUnavailable(f"Папка не найдена: {folder}")

        self._entries = sorted(
            item.relative_to(self._base).as_posix()
            for item in self._base.rglob("*")
            if item.is_file() and not is_service_file(item.name)
        )

    def entries(self) -> list[str]:
        return list(self._entries)

    def load(self, path: str) -> bytes:
        try:
            return (self._base / path).read_bytes()
        except FileNotFoundError:
            raise SourceUnavailable(f"В пакете нет файла: {path}")
