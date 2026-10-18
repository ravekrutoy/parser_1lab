import unittest

from domain import MalformedTask
from readers import CatsReader
from readers.cats.ranks import expand_rank
from readers.cats.sections import MEMORY
from storage import ZipFileSource, mount
from tests.support import PROJECT, SAMPLES, ArchiveFixture


class CatsSampleTest(unittest.TestCase):

    def check_area51(self, source):
        task = CatsReader().read(source)

        self.assertEqual(task.heading, "Area 51")
        self.assertEqual(task.writer, "NEERC 2005")
        self.assertEqual(task.cpu_ms, 2000)
        self.assertEqual(task.ram_bytes, 64 * 1024 ** 2)
        self.assertEqual(task.stdin_name, "area.in")
        self.assertEqual(task.stdout_name, "area.out")
        self.assertEqual(task.verifier, "check.dpr")
        self.assertEqual(task.references[0].origin, "area_al.dpr")
        self.assertEqual(len(task.cases), 42)
        self.assertEqual(task.cases[0].feed, "tests/01")
        self.assertEqual(task.cases[41].feed, "tests/42")
        self.assertEqual(task.cases[0].expected, "<решение 'sol'>")
        self.assertTrue(task.legend.startswith("Michael and Nick"))
        self.assertEqual(task.remarks, [])

    def test_zip(self):
        self.check_area51(ZipFileSource(str(SAMPLES / "cats_area51.zip")))

    def test_folder(self):
        self.check_area51(mount(str(PROJECT / "5298" / "CATS")))


class CatsEdgeCasesTest(ArchiveFixture):

    def read(self, body: str, attributes: str = 'title="T" tlimit="1" mlimit="1"',
             extra_files: dict | None = None):
        xml = f'<?xml version="1.0"?><CATS><Problem {attributes}>{body}</Problem></CATS>'
        files = {"problem.xml": xml, **(extra_files or {})}
        return CatsReader().read(ZipFileSource(self.pack(files)))

    def test_no_xml(self):
        with self.assertRaises(MalformedTask):
            CatsReader().read(ZipFileSource(self.pack({"a.txt": ""})))

    def test_two_xml_files(self):
        with self.assertRaises(MalformedTask):
            CatsReader().read(ZipFileSource(self.pack({"a.xml": "<CATS/>", "b.xml": "<CATS/>"})))

    def test_windows_1251(self):
        xml = '<?xml version="1.0" encoding="Windows-1251"?><CATS><Problem title="Задача"/></CATS>'
        path = self.pack({"p.xml": xml.encode("cp1251")})
        self.assertEqual(CatsReader().read(ZipFileSource(path)).heading, "Задача")

    def test_limits(self):
        task = self.read("", 'title="T" tlimit="0.5" mlimit="512K"')
        self.assertEqual(task.cpu_ms, 500)
        self.assertEqual(task.ram_bytes, 512 * 1024)

    def test_std_checker_and_interactor(self):
        task = self.read(
            '<Interactor name="i" src="i.cpp"/><Run method="interactive"/>',
            'title="T" stdChecker="nums"',
            {"i.cpp": ""},
        )
        self.assertEqual(task.verifier, "стандартный: nums")
        self.assertEqual(task.mediator, "i.cpp")
        self.assertIn("интерактив", task.execution_mode)

    def test_cases_merged_from_several_tags(self):
        task = self.read(
            '<Test rank="*" points="1"/>'
            '<Test rank="1-4"><In src="t/%0n.in"/><Out src="t/%n.out"/></Test>'
            '<Test rank="1-3-2" points="5"/>',
            extra_files={f"t/0{n}.in": "" for n in range(1, 5)}
            | {f"t/{n}.out": "" for n in range(1, 5)},
        )
        self.assertEqual([case.score for case in task.cases], [5, 1, 5, 1])
        self.assertEqual(task.cases[3].feed, "t/04.in")
        self.assertEqual(task.cases[3].expected, "t/4.out")
        self.assertEqual(task.remarks, [])

    def test_testsets(self):
        task = self.read(
            '<Test rank="1-5"><In>1</In><Out>1</Out></Test>'
            '<Testset name="easy" tests="1-2" points="10"/>'
            '<Testset name="all" tests="easy,3-5" depends_on="1-2" comment="c"/>'
        )
        easy, every = task.subtasks
        self.assertEqual(easy.score, 10)
        self.assertEqual(every.members, [1, 2, 3, 4, 5])
        self.assertEqual(every.depends_on, ["1-2"])
        self.assertEqual([case.subtask for case in task.cases], ["easy"] * 2 + ["all"] * 3)
        self.assertEqual(task.cases[0].feed, "<текст в XML>")

    def test_gap_in_ordinals_and_missing_files(self):
        task = self.read('<Test rank="1,3"><In src="x"/><Out use="sol"/></Test>')
        text = "\n".join(task.remarks)
        self.assertIn("подряд", text)
        self.assertIn("нет файла x", text)


class CatsNotationTest(unittest.TestCase):

    def test_expand_rank(self):
        self.assertEqual(expand_rank("1,3,5-7,10-16-3", {}), [1, 3, 5, 6, 7, 10, 13, 16])
        self.assertEqual(expand_rank("s,9", {"s": [1, 2]}), [1, 2, 9])
        for broken in ("1-x", "5-1-0", "1-2-3-4"):
            with self.subTest(spec=broken), self.assertRaises(MalformedTask):
                expand_rank(broken, {})

    def test_memory(self):
        self.assertEqual(MEMORY.to_bytes("64", "m"), 64 * 1024 ** 2)
        self.assertEqual(MEMORY.to_bytes("100B", "m"), 100)
        self.assertEqual(MEMORY.to_bytes("2k", "m"), 2048)
        self.assertIsNone(MEMORY.to_bytes(None, "m"))
        with self.assertRaises(MalformedTask):
            MEMORY.to_bytes("lots", "m")


if __name__ == "__main__":
    unittest.main()
