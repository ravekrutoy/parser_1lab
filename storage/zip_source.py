import zipfile

from domain import SourceUnavailable
from storage.hygiene import is_service_file, wrapping_folder
from storage.source import FileSource


class ZipFileSource(FileSource):

    def __init__(self, archive_path: str):
        try:
            self._zip = zipfile.ZipFile(archive_path)
        except FileNotFoundError:
            raise SourceUnavailable(f"Файл не найден: {archive_path}")
        except zipfile.BadZipFile:
            raise SourceUnavailable(f"Файл не является ZIP-архивом: {archive_path}")

        members = [
            member
            for member in self._zip.namelist()
            if not member.endswith("/") and not is_service_file(member)
        ]

        self._shift = wrapping_folder(members)
        self._entries = [member[len(self._shift):] for member in members]

    def entries(self) -> list[str]:
        return list(self._entries)

    def load(self, path: str) -> bytes:
        try:
            return self._zip.read(self._shift + path)
        except KeyError:
            raise SourceUnavailable(f"В пакете нет файла: {path}")
