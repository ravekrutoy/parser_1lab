import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain import HelperProgram, TaskDescriptor
from readers.toolkit.integrity import FileAudit
from readers.toolkit.quantities import GIB, KIB, MIB, SizeNotation
from readers.toolkit.scalars import real_number, seconds_to_ms


@dataclass
class CatsScope:
    node: ET.Element
    task: TaskDescriptor
    audit: FileAudit


class CatsSection(ABC):

    @abstractmethod
    def apply(self, scope: CatsScope) -> None:
        ...


MEMORY = SizeNotation({"B": 1, "K": KIB, "M": MIB, "G": GIB}, bare_factor=MIB)

PLAIN_ATTRIBUTES = {
    "lang": "Языки условия",
    "wlimit": "Лимит записи",
    "maxPoints": "Максимальный балл",
    "difficulty": "Сложность",
}


class HeaderSection(CatsSection):

    def apply(self, scope: CatsScope) -> None:
        node, task = scope.node, scope.task
        task.heading = node.get("title")
        task.writer = node.get("author")
        task.stdin_name = node.get("inputFile")
        task.stdout_name = node.get("outputFile")
        task.cpu_ms = seconds_to_ms(real_number(node.get("tlimit"), "tlimit"))
        task.ram_bytes = MEMORY.to_bytes(node.get("mlimit"), "mlimit")

        for attribute, caption in PLAIN_ATTRIBUTES.items():
            if node.get(attribute):
                task.specifics[caption] = node.get(attribute)

        codes = [keyword.get("code") for keyword in node.findall("Keyword")]
        if codes:
            task.specifics["Ключевые слова"] = ", ".join(filter(None, codes))

        examples = node.findall("Sample")
        if examples:
            task.specifics["Примеров в условии"] = str(len(examples))


class StatementSection(CatsSection):

    PREVIEW = 300

    def apply(self, scope: CatsScope) -> None:
        statement = scope.node.find("ProblemStatement")
        if statement is None:
            return

        reference = statement.get("url") or statement.get("attachment")
        if reference:
            scope.task.legend = reference
            return

        flat = " ".join("".join(statement.itertext()).split())
        if len(flat) > self.PREVIEW:
            flat = flat[:self.PREVIEW].rstrip() + "…"
        scope.task.legend = flat or None


LAUNCH_METHODS = {
    "default": "обычный запуск решения",
    "interactive": "интерактивный (решение + интерактор)",
    "competitive": "соревновательный (контроллер + агенты)",
}


class ToolingSection(CatsSection):

    def apply(self, scope: CatsScope) -> None:
        self._verifier(scope)
        self._mediator(scope)

        launch = scope.node.find("Run")
        method = launch.get("method", "default") if launch is not None else "default"
        scope.task.execution_mode = LAUNCH_METHODS.get(method, method)

        for node in scope.node.findall("Solution"):
            program = HelperProgram(role=node.get("name", "?"), origin=node.get("src"))
            scope.task.references.append(program)
            scope.audit.require_if_given(program.origin, f"решение {program.role}")

        producers = scope.node.findall("Generator") + scope.node.findall("GeneratorRange")
        if producers:
            scope.task.specifics["Генераторов"] = str(len(producers))

    def _verifier(self, scope: CatsScope) -> None:
        builtin = scope.node.get("stdChecker")
        custom = scope.node.find("Checker")
        imported = scope.node.find("Import[@type='checker']")

        if builtin:
            scope.task.verifier = f"стандартный: {builtin}"
        elif custom is not None:
            scope.task.verifier = custom.get("src")
            if custom.get("style"):
                scope.task.specifics["Стиль чекера"] = custom.get("style")
            scope.audit.require_if_given(custom.get("src"), "чекер")
        elif imported is not None:
            scope.task.verifier = f"импорт: {imported.get('guid')}"

    def _mediator(self, scope: CatsScope) -> None:
        node = scope.node.find("Interactor")
        if node is not None:
            scope.task.mediator = node.get("src")
            scope.audit.require_if_given(node.get("src"), "интерактор")
