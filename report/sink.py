import sys
from typing import TextIO


class TextSink:

    def __init__(self, stream: TextIO | None = None):
        self._stream = stream

    def line(self, text: str) -> None:
        print(text, file=self._stream or sys.stdout)

    def banner(self, title: str) -> None:
        self.line(f"\n========== {title} ==========")

    def pair(self, caption: str, value, indent: int = 0) -> None:
        if value is not None and value != "":
            self.line(f"{' ' * indent}{caption}: {value}")
