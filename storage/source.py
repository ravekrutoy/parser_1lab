from abc import ABC, abstractmethod


class FileSource(ABC):

    @abstractmethod
    def entries(self) -> list[str]:
        ...

    @abstractmethod
    def load(self, path: str) -> bytes:
        ...
