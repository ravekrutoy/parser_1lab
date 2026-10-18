from abc import ABC, abstractmethod

from domain import TaskDescriptor


class TaskRenderer(ABC):

    @abstractmethod
    def render(self, task: TaskDescriptor) -> None:
        ...
