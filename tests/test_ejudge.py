import unittest

from domain import MalformedTask
from readers import EjudgeReader
from readers.ejudge.naming import TestNaming
from readers.ejudge.reader import MEMORY
from storage import ZipFileSource
from tests.support import SAMPLES, ArchiveFixture


class EjudgeSampleTest(unittest.TestCase):

    def test_sample(self):
        task = EjudgeReader().read(ZipFileSource(str(SAMPLES / "ejudge_sample.zip")))

        self.assertEqual(task.heading, "Разработка задач")
        self.assertEqual(task.cpu_ms, 2000)
        self.assertEqual(task.ram_bytes, 512 * 1024 ** 2)
        self.assertEqual(task.stdin_name, "*STDIN")
        self.assertEqual(task.verifier, "checker")
        self.assertEqual(task.references[0].origin, "sol_ik_ac")
        self.assertEqual(task.specifics["Внутреннее имя"], "reconstruct-bus-schedule")
        self.assertEqual(task.specifics["valuer: stat_to_users"], "1")

        self.assertEqual([subtask.key for subtask in task.subtasks], ["0", "1", "2", "3", "4"])
        self.assertEqual([subtask.score for subtask in task.subtasks], [0, 10, 20, 40, 30])
        self.assertEqual(task.subtasks[3].members, list(range(16, 32)))
        self.assertEqual(task.subtasks[4].depends_on, ["3"])

        self.assertEqual(len(task.cases), 46)
        self.assertEqual(task.cases[8].feed, "tests/09")
        self.assertEqual(task.cases[8].expected, "tests/09.a")
        self.assertEqual(task.cases[8].subtask, "2")
        self.assertEqual(len(task.remarks), 1)


class EjudgeEdgeCasesTest(ArchiveFixture):

    SETTINGS = '[problem]\ntest_pat = "%02d.in"\ncorr_pat = "%02d.out"\n'

    def read(self, files: dict[str, str]):
        return EjudgeReader().read(ZipFileSource(self.pack(files)))

    def test_missing_settings(self):
        with self.assertRaises(MalformedTask):
            self.read({"valuer.cfg": ""})

    def test_settings_without_section(self):
        with self.assertRaises(MalformedTask):
            self.read({"problem.cfg": "time_limit = 1\n"})

    def test_settings_values(self):
        task = self.read({"problem.cfg": (
            "# комментарий\n[contest]\nlong_name = \"не та секция\"\n"
            "[problem]\nlong_name = \"Задача\"\ntime_limit = 1\ntime_limit_millis = 1500\n"
            "max_vm_size = 65536K\nuse_stdin\ninput_file = \"a.in\"\nstandard_checker = cmp_int\n"
        )})
        self.assertEqual(task.heading, "Задача")
        self.assertEqual(task.cpu_ms, 1500)
        self.assertEqual(task.ram_bytes, 64 * 1024 ** 2)
        self.assertEqual(task.stdin_name, "*STDIN")
        self.assertEqual(task.verifier, "стандартный: cmp_int")
        self.assertEqual(task.remarks, [])

    def test_cases_from_files_without_valuer(self):
        files = {"problem.cfg": self.SETTINGS}
        for ordinal in (1, 2, 3):
            files[f"tests/0{ordinal}.in"] = ""
            files[f"tests/0{ordinal}.out"] = ""
        files["tests/readme.txt"] = ""

        task = self.read(files)
        self.assertEqual([case.feed for case in task.cases],
                         ["tests/01.in", "tests/02.in", "tests/03.in"])
        self.assertEqual(task.subtasks, [])
        self.assertEqual(task.remarks, [])

    def test_valuer_options_and_comments(self):
        task = self.read({
            "problem.cfg": self.SETTINGS,
            "valuer.cfg": (
                "# комментарий\n"
                "group 1 { tests 1-2; score 5; }  # еще комментарий\n"
                "group 2 {\n tests 3 - 4;\n test_score 3;\n requires 1, 7;\n offline;\n"
                " user_status \"OK\";\n 0_if 3, 4;\n}\n"
            ),
            "tests/01.in": "", "tests/01.out": "",
        })
        first, second = task.subtasks
        self.assertEqual(first.score, 5)
        self.assertEqual(second.members, [3, 4])
        self.assertEqual(second.depends_on, ["1", "7"])
        self.assertIn("offline", second.note)
        self.assertEqual([case.score for case in task.cases], [None, None, 3, 3])

        text = "\n".join(task.remarks)
        self.assertIn("несуществующей группы 7", text)
        self.assertIn("нет файла tests/02.in", text)

    def test_overlapping_groups(self):
        task = self.read({
            "problem.cfg": self.SETTINGS,
            "valuer.cfg": "group 1 { tests 1-3; } group 2 { tests 3-4; }",
        })
        self.assertIn("входит в группы 1 и 2", "\n".join(task.remarks))

    def test_valuer_syntax_errors(self):
        for valuer in (
            "group 1 { tests 1-2 }",
            "group 1 { tests 1-2;",
            "group x { }",
            "group 1 { tests 5-2; }",
            "group 1 { score a; }",
            "group 1 { tests 1-2; } @",
            "groop 1 { }",
        ):
            with self.subTest(valuer=valuer):
                with self.assertRaises(MalformedTask):
                    self.read({"problem.cfg": self.SETTINGS, "valuer.cfg": valuer})

    def test_helpers(self):
        self.assertEqual(MEMORY.to_bytes("512M", "m"), 512 * 1024 ** 2)
        self.assertEqual(MEMORY.to_bytes("1000", "m"), 1000)
        naming = TestNaming("%02d.a")
        self.assertEqual(naming.ordinal_of("07.a"), 7)
        self.assertIsNone(naming.ordinal_of("07"))
        self.assertEqual(naming.name_for(7), "07.a")
        self.assertEqual(TestNaming("t/###").name_for(7), "t/007")


if __name__ == "__main__":
    unittest.main()
