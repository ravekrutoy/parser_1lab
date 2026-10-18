import re

from domain import MalformedTask


class TestNaming:

    __test__ = False

    def __init__(self, template: str):
        self.template = template
        self._matcher: re.Pattern | None = None

    def name_for(self, ordinal: int) -> str:
        hashes = re.search(r"#+", self.template)
        if hashes and "%" not in self.template:
            width = len(hashes.group())
            return self.template[:hashes.start()] + f"{ordinal:0{width}d}" + self.template[hashes.end():]

        try:
            return self.template % ordinal
        except (TypeError, ValueError):
            raise self._invalid()

    def ordinal_of(self, file_name: str) -> int | None:
        found = self._compiled().fullmatch(file_name)
        return int(found.group(1)) if found else None

    def _compiled(self) -> re.Pattern:
        if self._matcher is None:
            halves = re.split(r"%0?\d*d", self.template, maxsplit=1)
            if len(halves) != 2:
                raise self._invalid()
            self._matcher = re.compile(re.escape(halves[0]) + r"(\d+)" + re.escape(halves[1]))
        return self._matcher

    def _invalid(self) -> MalformedTask:
        return MalformedTask(f"Некорректный шаблон имени теста '{self.template}'")
