import re
from dataclasses import dataclass, field
from typing import Callable

from domain import MalformedTask, Subtask


@dataclass
class ValuerOutcome:
    global_options: dict[str, str] = field(default_factory=dict)
    subtasks: list[Subtask] = field(default_factory=list)
    per_case_score: dict[str, int] = field(default_factory=dict)


class ValuerLexer:

    LEXEME = re.compile(r'\s*(?:([A-Za-z0-9_]+)|"([^"]*)"|([{};,\-]))')

    def __init__(self, label: str):
        self._label = label

    def split(self, text: str) -> list[str]:
        lexemes = []
        for row, line in enumerate(text.splitlines(), start=1):
            line = line.split("#", 1)[0]
            cursor = 0
            while cursor < len(line) and line[cursor:].strip():
                found = self.LEXEME.match(line, cursor)
                if found is None:
                    raise MalformedTask(
                        f"{self._label}, строка {row}: "
                        f"непонятный символ '{line[cursor:].strip()[0]}'"
                    )
                lexemes.append(found.group(found.lastindex))
                cursor = found.end()
        return lexemes


class LexemeStream:

    def __init__(self, lexemes: list[str], label: str):
        self._lexemes = lexemes
        self._index = 0
        self._label = label

    def peek(self) -> str | None:
        return self._lexemes[self._index] if self._index < len(self._lexemes) else None

    def take(self) -> str:
        current = self.peek()
        if current is None:
            raise self.failure("неожиданный конец файла")
        self._index += 1
        return current

    def demand(self, expected: str) -> None:
        current = self.take()
        if current != expected:
            raise self.failure(f"ожидалось '{expected}', получено '{current}'")

    def statement_tail(self, brace_ends: bool = False) -> list[str]:
        collected = []
        while True:
            current = self.peek()
            if current is None:
                raise self.failure("неожиданный конец файла, ожидалась ';'")
            if current == ";":
                self.take()
                return collected
            if current == "}" and brace_ends:
                return collected
            if current in "{}":
                raise self.failure(f"ожидалась ';', получено '{current}'")
            collected.append(self.take())

    def failure(self, message: str) -> MalformedTask:
        return MalformedTask(f"{self._label}: {message}")


OptionHandler = Callable[[LexemeStream, Subtask, list[str], ValuerOutcome], None]


def _single_number(stream: LexemeStream, values: list[str], option: str) -> int:
    if len(values) != 1 or not values[0].lstrip("-").isdigit():
        raise stream.failure(f"{option}: ожидалось одно число, получено '{' '.join(values)}'")
    return int(values[0])


def _tests_option(stream: LexemeStream, subtask: Subtask, values: list[str], _: ValuerOutcome) -> None:
    if len(values) == 3 and values[1] == "-" and values[0].isdigit() and values[2].isdigit():
        low, high = int(values[0]), int(values[2])
    elif len(values) == 1 and values[0].isdigit():
        low = high = int(values[0])
    else:
        raise stream.failure(f"группа {subtask.key}: некорректный диапазон тестов '{' '.join(values)}'")

    if low > high:
        raise stream.failure(f"группа {subtask.key}: начало диапазона {low} больше конца {high}")
    subtask.members = list(range(low, high + 1))


def _score_option(stream: LexemeStream, subtask: Subtask, values: list[str], _: ValuerOutcome) -> None:
    subtask.score = _single_number(stream, values, "score")


def _test_score_option(stream: LexemeStream, subtask: Subtask, values: list[str], outcome: ValuerOutcome) -> None:
    outcome.per_case_score[subtask.key] = _single_number(stream, values, "test_score")


def _requires_option(_: LexemeStream, subtask: Subtask, values: list[str], __: ValuerOutcome) -> None:
    subtask.depends_on = [value for value in values if value != ","]


class ValuerGrammar:

    HANDLERS: dict[str, OptionHandler] = {
        "tests": _tests_option,
        "score": _score_option,
        "test_score": _test_score_option,
        "requires": _requires_option,
    }

    def __init__(self, text: str, label: str):
        self._stream = LexemeStream(ValuerLexer(label).split(text), label)

    def parse(self) -> ValuerOutcome:
        outcome = ValuerOutcome()

        if self._stream.peek() == "global":
            self._stream.take()
            outcome.global_options = self._global_block()

        while self._stream.peek() is not None:
            self._stream.demand("group")
            outcome.subtasks.append(self._group_block(outcome))

        return outcome

    def _global_block(self) -> dict[str, str]:
        options = {}
        self._stream.demand("{")
        while self._stream.peek() != "}":
            name = self._stream.take()
            options[name] = " ".join(self._stream.statement_tail(brace_ends=True)) or "да"
        self._stream.demand("}")
        return options

    def _group_block(self, outcome: ValuerOutcome) -> Subtask:
        key = self._stream.take()
        if not key.isdigit():
            raise self._stream.failure(f"номер группы должен быть числом, получено '{key}'")

        subtask = Subtask(key=key)
        leftovers = []

        self._stream.demand("{")
        while self._stream.peek() != "}":
            option = self._stream.take()
            values = self._stream.statement_tail()
            handler = self.HANDLERS.get(option)
            if handler is not None:
                handler(self._stream, subtask, values, outcome)
            else:
                leftovers.append(option + (" " + "".join(values) if values else ""))
        self._stream.demand("}")

        if leftovers:
            subtask.note = "; ".join(leftovers)
        return subtask
