from abc import ABC, abstractmethod

from domain import TaskDescriptor
from storage import FileSource


class TaskReader(ABC):

    dialect: str

    @abstractmethod
    def read(self, source: FileSource) -> TaskDescriptor:
        ...
