from typing import TextIO

from domain import TaskDescriptor
from report.blocks import (
    CasesBlock,
    OverviewBlock,
    ReferencesBlock,
    RemarksBlock,
    ReportBlock,
    ScoreTotalBlock,
    SubtasksBlock,
)
from report.contract import TaskRenderer
from report.sink import TextSink


class TextReport(TaskRenderer):

    def __init__(self, stream: TextIO | None = None, blocks: list[ReportBlock] | None = None):
        self._sink = TextSink(stream)
        self._blocks = blocks or [
            OverviewBlock(),
            ReferencesBlock(),
            SubtasksBlock(),
            CasesBlock(),
            ScoreTotalBlock(),
            RemarksBlock(),
        ]

    def render(self, task: TaskDescriptor) -> None:
        for block in self._blocks:
            block.write(task, self._sink)
