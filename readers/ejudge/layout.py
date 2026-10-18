from posixpath import join

from domain import Case, TaskDescriptor
from readers.ejudge.naming import TestNaming
from readers.toolkit.integrity import FileAudit
from storage import SourceView


class CaseLayout:

    def __init__(self, view: SourceView, base: str, settings: dict[str, str]):
        self._view = view
        self._base = base
        self._folder = settings.get("test_dir", "tests")
        self._feed = TestNaming(settings.get("test_pat") or "%03d" + settings.get("test_sfx", ""))
        self._answer = TestNaming(settings.get("corr_pat") or "%03d" + settings.get("corr_sfx", ".ans"))

    def populate(self, task: TaskDescriptor, per_case_score: dict[str, int]) -> None:
        location = join(self._base, self._folder)
        present = self._files_in(location)

        ordinals = {self._feed.ordinal_of(name) for name in present} - {None}
        for subtask in task.subtasks:
            ordinals.update(subtask.members)

        owner_of = self._owners(task)
        for ordinal in sorted(ordinals):
            task.cases.append(Case(
                ordinal=ordinal,
                feed=join(self._folder, self._feed.name_for(ordinal)),
                expected=join(self._folder, self._answer.name_for(ordinal)),
                subtask=owner_of.get(ordinal),
                score=per_case_score.get(owner_of.get(ordinal)),
            ))

        if ordinals and ordinals != set(range(1, max(ordinals) + 1)):
            task.remark("Номера тестов должны идти подряд, начиная с 1")

        if not present:
            if task.cases:
                task.remark(f"Папка {location}/ пуста или отсутствует, файлы тестов не проверены")
            return

        FileAudit(self._view, task, self._base).require_case_files()

    def _files_in(self, location: str) -> set[str]:
        prefix = location + "/"
        return {entry[len(prefix):] for entry in self._view.entries() if entry.startswith(prefix)}

    @staticmethod
    def _owners(task: TaskDescriptor) -> dict[int, str]:
        owner_of: dict[int, str] = {}
        for subtask in task.subtasks:
            for ordinal in subtask.members:
                if ordinal in owner_of:
                    task.remark(f"Тест №{ordinal} входит в группы {owner_of[ordinal]} и {subtask.key}")
                else:
                    owner_of[ordinal] = subtask.key
        return owner_of
