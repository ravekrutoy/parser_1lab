import argparse
import sys
from typing import Callable, TextIO

from domain import RejectedInput
from readers import ReaderCatalog
from report import TaskRenderer
from storage import FileSource


class ConsoleApp:

    def __init__(
        self,
        catalog: ReaderCatalog,
        opener: Callable[[str], FileSource],
        renderer: TaskRenderer,
        errors: TextIO | None = None,
    ):
        self._catalog = catalog
        self._opener = opener
        self._renderer = renderer
        self._errors = errors

    def run(self, argv: list[str] | None = None) -> int:
        options = self._options().parse_args(argv)
        try:
            reader = self._catalog.pick(options.format)
            source = self._opener(options.package)
            task = reader.read(source)
        except RejectedInput as failure:
            print(f"Ошибка: {failure}", file=self._errors or sys.stderr)
            return 1

        self._renderer.render(task)
        return 0

    def _options(self) -> argparse.ArgumentParser:
        options = argparse.ArgumentParser(
            description="Разбор пакета задачи олимпиады по программированию",
        )
        options.add_argument(
            "format", metavar="FORMAT",
            help=f"формат пакета: {', '.join(self._catalog.dialects())}",
        )
        options.add_argument(
            "package", metavar="PACKAGE",
            help="путь к ZIP-архиву (или распакованной папке)",
        )
        return options
