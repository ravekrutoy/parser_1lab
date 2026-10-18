import xml.etree.ElementTree as ET

from domain import MalformedTask, TaskDescriptor
from readers.cats.cases import CaseSection
from readers.cats.sections import CatsScope, CatsSection, HeaderSection, StatementSection, ToolingSection
from readers.contract import TaskReader
from readers.toolkit.integrity import FileAudit
from readers.toolkit.xmltools import parse_tree
from storage import FileSource, SourceView


class CatsReader(TaskReader):

    dialect = "CATS"

    def __init__(self, sections: list[CatsSection] | None = None):
        self._sections = sections or [
            HeaderSection(),
            StatementSection(),
            ToolingSection(),
            CaseSection(),
        ]

    def read(self, source: FileSource) -> TaskDescriptor:
        view = SourceView(source)
        manifest = self._manifest_path(view)
        tree = parse_tree(view.raw(manifest), manifest)
        node = self._problem_node(tree, manifest)

        task = TaskDescriptor(dialect=self.dialect)
        task.specifics["Файл описания"] = manifest
        task.specifics["Версия формата"] = tree.get("version", "1.4")

        scope = CatsScope(node=node, task=task, audit=FileAudit(view, task))
        for section in self._sections:
            section.apply(scope)
        return task

    def _manifest_path(self, view: SourceView) -> str:
        candidates = [entry for entry in view.top_level() if entry.lower().endswith(".xml")]
        if not candidates:
            raise MalformedTask("В корне пакета CATS нет XML-файла с описанием задачи")
        if len(candidates) > 1:
            raise MalformedTask(
                "В корне пакета CATS должен быть ровно один XML-файл, найдено: "
                + ", ".join(candidates)
            )
        return candidates[0]

    def _problem_node(self, tree: ET.Element, manifest: str) -> ET.Element:
        if tree.tag != "CATS":
            raise MalformedTask(f"Корневой тег {manifest} должен быть <CATS>")
        node = tree.find("Problem")
        if node is None:
            raise MalformedTask(f"В {manifest} нет тега <Problem>")
        return node
