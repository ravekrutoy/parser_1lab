from pathlib import PurePosixPath

from storage.source import FileSource


class SourceView:

    def __init__(self, source: FileSource):
        self._source = source

    def entries(self) -> list[str]:
        return self._source.entries()

    def contains(self, path: str) -> bool:
        return path in self._source.entries()

    def raw(self, path: str) -> bytes:
        return self._source.load(path)

    def text(self, path: str, encoding: str = "utf-8") -> str:
        return self._source.load(path).decode(encoding)

    def locate(self, file_name: str) -> list[str]:
        wanted = file_name.lower()
        hits = [
            entry
            for entry in self._source.entries()
            if PurePosixPath(entry).name.lower() == wanted
        ]
        return sorted(hits, key=lambda entry: (entry.count("/"), entry))

    def top_level(self) -> list[str]:
        return [entry for entry in self._source.entries() if "/" not in entry]
