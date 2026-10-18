from abc import ABC, abstractmethod

from domain import TaskDescriptor
from report.formatting import compress_ordinals, describe_duration, describe_volume
from report.sink import TextSink


class ReportBlock(ABC):

    @abstractmethod
    def write(self, task: TaskDescriptor, sink: TextSink) -> None:
        ...


class OverviewBlock(ReportBlock):

    def write(self, task: TaskDescriptor, sink: TextSink) -> None:
        sink.banner("ИНФОРМАЦИЯ О ЗАДАЧЕ")
        sink.pair("Формат пакета", task.dialect)
        sink.pair("Название", task.heading)
        sink.pair("Автор", task.writer)
        sink.pair("Условие", task.legend)
        sink.pair("Лимит времени", describe_duration(task.cpu_ms))
        sink.pair("Лимит памяти", describe_volume(task.ram_bytes))
        sink.pair("Входной файл", task.stdin_name)
        sink.pair("Выходной файл", task.stdout_name)
        sink.pair("Проверяющая программа", task.verifier)
        sink.pair("Интерактор", task.mediator)
        sink.pair("Тип запуска", task.execution_mode)
        for caption, value in task.specifics.items():
            sink.pair(caption, value)


class ReferencesBlock(ReportBlock):

    def write(self, task: TaskDescriptor, sink: TextSink) -> None:
        if not task.references:
            return
        sink.banner("РЕШЕНИЯ")
        for program in task.references:
            sink.line(f"{program.role}: {program.origin or '-'}")


class SubtasksBlock(ReportBlock):

    def write(self, task: TaskDescriptor, sink: TextSink) -> None:
        if not task.subtasks:
            return
        sink.banner("ГРУППЫ ТЕСТОВ")
        for subtask in task.subtasks:
            sink.line(f"Группа {subtask.key}")
            sink.pair("Баллы", subtask.score, indent=2)
            sink.pair("Зависит от", ", ".join(subtask.depends_on) or "-", indent=2)
            sink.pair("Тесты", compress_ordinals(subtask.members) or "-", indent=2)
            sink.pair("Комментарий", subtask.note, indent=2)


class CasesBlock(ReportBlock):

    def write(self, task: TaskDescriptor, sink: TextSink) -> None:
        sink.banner(f"ТЕСТЫ ({len(task.cases)})")
        for case in task.cases:
            cells = [f"№{case.ordinal:<3}", f"{case.feed or '-'} -> {case.expected or '-'}"]
            if case.subtask is not None:
                cells.append(f"группа {case.subtask}")
            if case.score is not None:
                cells.append(f"баллы {case.score}")
            sink.line("  ".join(cells))


class ScoreTotalBlock(ReportBlock):

    def write(self, task: TaskDescriptor, sink: TextSink) -> None:
        total = sum(case.score or 0 for case in task.cases)
        total += sum(subtask.score or 0 for subtask in task.subtasks)
        sink.line(f"\nСумма баллов по тестам и группам: {total}")


class RemarksBlock(ReportBlock):

    def write(self, task: TaskDescriptor, sink: TextSink) -> None:
        if not task.remarks:
            return
        sink.banner(f"ПРЕДУПРЕЖДЕНИЯ ({len(task.remarks)})")
        for remark in task.remarks:
            sink.line(f"! {remark}")
