from posixpath import dirname, join

from domain import HelperProgram, MalformedTask, TaskDescriptor
from readers.contract import TaskReader
from readers.ejudge.layout import CaseLayout
from readers.ejudge.settings import read_problem_section
from readers.ejudge.valuer import ValuerGrammar
from readers.toolkit.integrity import flag_missing_dependencies
from readers.toolkit.quantities import GIB, KIB, MIB, SizeNotation
from readers.toolkit.scalars import real_number, seconds_to_ms, whole_number
from storage import FileSource, SourceView


SETTINGS_FILE = "problem.cfg"
VALUER_FILE = "valuer.cfg"

BUILTIN_PREFIX = "стандартный:"

MEMORY = SizeNotation({"K": KIB, "M": MIB, "G": GIB}, bare_factor=1)

VERBATIM_KEYS = {
    "long_name_en": "Название (англ.)",
    "internal_name": "Внутреннее имя",
    "short_name": "Короткое имя",
    "extid": "Внешний идентификатор",
    "revision": "Ревизия",
    "full_score": "Полный балл",
    "enable_testlib_mode": "Режим testlib",
    "use_corr": "Есть файлы ответов",
}


class EjudgeReader(TaskReader):

    dialect = "EJUDGE"

    def read(self, source: FileSource) -> TaskDescriptor:
        view = SourceView(source)
        settings_path = self._settings_path(view)
        base = dirname(settings_path)
        settings = read_problem_section(view.text(settings_path), settings_path)

        task = TaskDescriptor(dialect=self.dialect)
        self._apply_settings(settings, task)
        per_case_score = self._apply_valuer(view, join(base, VALUER_FILE), task)

        CaseLayout(view, base, settings).populate(task, per_case_score)
        flag_missing_dependencies(task)
        self._audit_programs(view, base, task)
        return task

    def _settings_path(self, view: SourceView) -> str:
        found = view.locate(SETTINGS_FILE)
        if not found:
            raise MalformedTask(f"В пакете EJUDGE нет файла {SETTINGS_FILE}")
        return found[0]

    def _apply_settings(self, settings: dict[str, str], task: TaskDescriptor) -> None:
        task.heading = settings.get("long_name") or settings.get("short_name")
        if settings.get("check_cmd"):
            task.verifier = settings["check_cmd"]
        elif settings.get("standard_checker"):
            task.verifier = f"{BUILTIN_PREFIX} {settings['standard_checker']}"
        task.mediator = settings.get("interactor_cmd")

        task.cpu_ms = whole_number(settings.get("time_limit_millis"), "time_limit_millis")
        if task.cpu_ms is None:
            task.cpu_ms = seconds_to_ms(real_number(settings.get("time_limit"), "time_limit"))

        task.ram_bytes = MEMORY.to_bytes(settings.get("max_vm_size"), "max_vm_size")

        task.stdin_name = "*STDIN" if settings.get("use_stdin") == "1" else settings.get("input_file")
        task.stdout_name = "*STDOUT" if settings.get("use_stdout") == "1" else settings.get("output_file")

        if settings.get("solution_cmd"):
            task.references.append(HelperProgram(role="эталонное", origin=settings["solution_cmd"]))

        for key, caption in VERBATIM_KEYS.items():
            if settings.get(key):
                task.specifics[caption] = settings[key]

    def _apply_valuer(self, view: SourceView, path: str, task: TaskDescriptor) -> dict[str, int]:
        if not view.contains(path):
            return {}

        outcome = ValuerGrammar(view.text(path), path).parse()
        task.subtasks = outcome.subtasks
        task.execution_mode = "группы тестов (valuer.cfg)"
        for name, value in outcome.global_options.items():
            task.specifics[f"valuer: {name}"] = value
        return outcome.per_case_score

    def _audit_programs(self, view: SourceView, base: str, task: TaskDescriptor) -> None:
        programs = [("чекер", task.verifier), ("интерактор", task.mediator)]
        programs += [("решение", program.origin) for program in task.references]

        entries = set(view.entries())
        for owner, command in programs:
            if not command or command.startswith(BUILTIN_PREFIX):
                continue
            path = join(base, command)
            if path not in entries and not any(entry.startswith(path + ".") for entry in entries):
                task.remark(f"{owner}: нет файла {command} (или его исходника)")
