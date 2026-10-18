from dataclasses import dataclass, field


@dataclass
class Case:
    ordinal: int
    feed: str | None = None
    expected: str | None = None
    subtask: str | None = None
    score: int | None = None


@dataclass
class Subtask:
    key: str
    score: int | None = None
    depends_on: list[str] = field(default_factory=list)
    members: list[int] = field(default_factory=list)
    note: str | None = None


@dataclass
class HelperProgram:
    role: str
    origin: str | None = None


@dataclass
class TaskDescriptor:
    dialect: str

    heading: str | None = None
    writer: str | None = None
    legend: str | None = None

    cpu_ms: int | None = None
    ram_bytes: int | None = None

    stdin_name: str | None = None
    stdout_name: str | None = None

    verifier: str | None = None
    mediator: str | None = None
    execution_mode: str | None = None

    references: list[HelperProgram] = field(default_factory=list)
    subtasks: list[Subtask] = field(default_factory=list)
    cases: list[Case] = field(default_factory=list)

    specifics: dict[str, str] = field(default_factory=dict)

    remarks: list[str] = field(default_factory=list)

    def remark(self, text: str) -> None:
        self.remarks.append(text)
