import xml.etree.ElementTree as ET
from posixpath import dirname

from domain import Case, MalformedTask, Subtask, TaskDescriptor
from readers.contract import TaskReader
from readers.toolkit.integrity import FileAudit, flag_missing_dependencies
from readers.toolkit.scalars import comma_items, whole_number
from readers.toolkit.xmltools import inner_text, parse_tree
from storage import FileSource, SourceView


MANIFEST = "testinfo.xml"

LAUNCH_MODES = {
    0: "до первого упавшего теста",
    1: "все тесты",
    2: "группы тестов",
}


class KrsuReader(TaskReader):

    dialect = "KRSU"

    def read(self, source: FileSource) -> TaskDescriptor:
        view = SourceView(source)
        manifest = self._manifest_path(view)
        tree = parse_tree(view.raw(manifest), manifest)
        if tree.tag != "testinfo":
            raise MalformedTask(f"Корневой тег {manifest} должен быть <testinfo>")

        task = TaskDescriptor(dialect=self.dialect)
        self._fill_header(tree, task)
        task.subtasks = [self._subtask(node) for node in tree.findall("group")]
        task.cases = [
            self._case(node, ordinal)
            for ordinal, node in enumerate(tree.findall("test"), start=1)
        ]

        self._attach_cases(task)
        flag_missing_dependencies(task)
        FileAudit(view, task, dirname(manifest)).require_case_files()
        return task

    def _manifest_path(self, view: SourceView) -> str:
        found = view.locate(MANIFEST)
        if not found:
            raise MalformedTask(f"В пакете KRSU нет файла {MANIFEST}")
        return found[0]

    def _fill_header(self, tree: ET.Element, task: TaskDescriptor) -> None:
        task.verifier = inner_text(tree, "checker")
        task.mediator = inner_text(tree, "interactor")
        task.legend = inner_text(tree, "problem")
        task.ram_bytes = whole_number(inner_text(tree, "memorylimit"), "memorylimit")
        task.cpu_ms = whole_number(inner_text(tree, "timelimit"), "timelimit")

        revision = inner_text(tree, "testversion")
        if revision is not None:
            task.specifics["Версия пакета"] = revision

        mode = whole_number(inner_text(tree, "runtype"), "runtype")
        if mode is not None:
            task.execution_mode = LAUNCH_MODES.get(mode, f"неизвестный ({mode})")

    def _subtask(self, node: ET.Element) -> Subtask:
        key = node.get("id")
        if not key:
            raise MalformedTask("У <group> не указан атрибут id")

        return Subtask(
            key=key.strip(),
            score=whole_number(node.get("points"), f"points группы {key}"),
            depends_on=comma_items(node.get("prereq")),
        )

    def _case(self, node: ET.Element, ordinal: int) -> Case:
        feed, expected = node.get("input"), node.get("output")
        if not feed or not expected:
            raise MalformedTask(f"У теста №{ordinal} должны быть атрибуты input и output")

        owner = node.get("groupid")
        return Case(
            ordinal=ordinal,
            feed=feed,
            expected=expected,
            subtask=owner.strip() if owner else None,
            score=whole_number(node.get("points"), f"points теста №{ordinal}"),
        )

    def _attach_cases(self, task: TaskDescriptor) -> None:
        by_key = {subtask.key: subtask for subtask in task.subtasks}
        for case in task.cases:
            if case.subtask is None:
                continue
            target = by_key.get(case.subtask)
            if target is None:
                task.remark(f"Тест №{case.ordinal} ссылается на несуществующую группу {case.subtask}")
            else:
                target.members.append(case.ordinal)
