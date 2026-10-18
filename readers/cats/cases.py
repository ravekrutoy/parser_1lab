import xml.etree.ElementTree as ET

from domain import Case, MalformedTask, Subtask, TaskDescriptor
from readers.cats.payload import describe_payload, names_a_file
from readers.cats.ranks import expand_rank
from readers.cats.sections import CatsScope, CatsSection
from readers.toolkit.scalars import comma_items, whole_number


WILDCARD = "*"


class CaseSection(CatsSection):

    def apply(self, scope: CatsScope) -> None:
        named_sets = self._named_sets(scope.node)
        scope.task.cases = CaseAssembler(scope.node, named_sets).assemble()
        scope.task.subtasks = self._subtasks(scope.node, named_sets, scope.task)
        self._verify(scope)

    def _named_sets(self, node: ET.Element) -> dict[str, list[int]]:
        named_sets: dict[str, list[int]] = {}
        for testset in node.findall("Testset"):
            title = testset.get("name")
            if not title:
                raise MalformedTask("У <Testset> не указан атрибут name")
            named_sets[title] = expand_rank(testset.get("tests", ""), named_sets)
        return named_sets

    def _subtasks(
        self,
        node: ET.Element,
        named_sets: dict[str, list[int]],
        task: TaskDescriptor,
    ) -> list[Subtask]:
        by_ordinal = {case.ordinal: case for case in task.cases}
        subtasks = []

        for testset in node.findall("Testset"):
            title = testset.get("name")
            subtask = Subtask(
                key=title,
                score=whole_number(testset.get("points"), f"points набора {title}"),
                depends_on=comma_items(testset.get("depends_on")),
                members=named_sets[title],
                note=testset.get("comment"),
            )
            subtasks.append(subtask)

            for ordinal in subtask.members:
                case = by_ordinal.get(ordinal)
                if case is None:
                    task.remark(f"Набор {title} содержит неописанный тест №{ordinal}")
                elif case.subtask is None:
                    case.subtask = title

        return subtasks

    def _verify(self, scope: CatsScope) -> None:
        task = scope.task
        ordinals = [case.ordinal for case in task.cases]
        if ordinals and ordinals != list(range(1, len(ordinals) + 1)):
            task.remark("Номера тестов должны идти подряд, начиная с 1")

        for case in task.cases:
            owner = f"Тест №{case.ordinal}"
            if case.feed is None:
                task.remark(f"{owner}: не задан входной файл")
            if case.expected is None:
                task.remark(f"{owner}: не задан выходной файл")

            for payload in (case.feed, case.expected):
                if names_a_file(payload):
                    scope.audit.require(payload, f"тест №{case.ordinal}")


class CaseAssembler:

    def __init__(self, node: ET.Element, named_sets: dict[str, list[int]]):
        self._node = node
        self._named_sets = named_sets
        self._cases: dict[int, Case] = {}

    def assemble(self) -> list[Case]:
        fallbacks = []
        for node in self._node.findall("Test"):
            rank = node.get("rank", "")
            if rank.strip() == WILDCARD:
                fallbacks.append(node)
            else:
                self._merge_into(node, expand_rank(rank, self._named_sets))

        for node in self._node.findall("TestRange"):
            first = whole_number(node.get("from"), "TestRange from")
            last = whole_number(node.get("to"), "TestRange to")
            if first is None or last is None:
                raise MalformedTask("У <TestRange> должны быть атрибуты from и to")
            self._merge_into(node, range(first, last + 1))

        for node in fallbacks:
            for case in self._cases.values():
                self._overlay(node, case, keep_existing=True)

        return [self._cases[ordinal] for ordinal in sorted(self._cases)]

    def _merge_into(self, node: ET.Element, ordinals) -> None:
        for ordinal in ordinals:
            self._overlay(node, self._cases.setdefault(ordinal, Case(ordinal)))

    @staticmethod
    def _overlay(node: ET.Element, case: Case, keep_existing: bool = False) -> None:
        score = whole_number(node.get("points"), f"points теста №{case.ordinal}")
        if score is not None and not (keep_existing and case.score is not None):
            case.score = score

        feed = node.find("In")
        if feed is not None and not (keep_existing and case.feed):
            case.feed = describe_payload(feed, case.ordinal, "генератор")

        expected = node.find("Out")
        if expected is not None and not (keep_existing and case.expected):
            case.expected = describe_payload(expected, case.ordinal, "решение")
