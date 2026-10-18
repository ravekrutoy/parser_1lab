from posixpath import join

from domain import TaskDescriptor
from storage import SourceView


class FileAudit:

    def __init__(self, view: SourceView, task: TaskDescriptor, base: str = ""):
        self._view = view
        self._task = task
        self._base = base

    def require(self, name: str, owner: str) -> None:
        if not self._view.contains(join(self._base, name)):
            self._task.remark(f"{owner}: нет файла {name}")

    def require_if_given(self, name: str | None, owner: str) -> None:
        if name:
            self.require(name, owner)

    def require_case_files(self) -> None:
        for case in self._task.cases:
            for name in (case.feed, case.expected):
                self.require(name, f"Тест №{case.ordinal}")


def flag_missing_dependencies(task: TaskDescriptor) -> None:
    known = {subtask.key for subtask in task.subtasks}
    for subtask in task.subtasks:
        for required in subtask.depends_on:
            if required not in known:
                task.remark(f"Группа {subtask.key} зависит от несуществующей группы {required}")
