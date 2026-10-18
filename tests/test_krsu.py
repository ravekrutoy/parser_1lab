import unittest

from domain import MalformedTask
from readers import KrsuReader
from storage import ZipFileSource
from tests.support import SAMPLES, ArchiveFixture


class KrsuSamplesTest(unittest.TestCase):

    def test_package_a(self):
        task = KrsuReader().read(ZipFileSource(str(SAMPLES / "krsu_A.zip")))

        self.assertEqual(task.verifier, "$fc")
        self.assertEqual(task.cpu_ms, 1000)
        self.assertEqual(task.ram_bytes, 256 * 1024 ** 2)
        self.assertEqual(task.execution_mode, "до первого упавшего теста")
        self.assertEqual(len(task.cases), 27)
        self.assertEqual(sum(case.score for case in task.cases), 100)
        self.assertEqual(task.cases[4].feed, "input05.txt")
        self.assertEqual(task.cases[4].score, 5)
        self.assertEqual(task.remarks, [])

    def test_package_with_groups(self):
        task = KrsuReader().read(ZipFileSource(str(SAMPLES / "krsu_groups.zip")))

        self.assertEqual(task.mediator, "interactor.exe")
        self.assertEqual(task.legend, "problem.tex")
        self.assertEqual([subtask.key for subtask in task.subtasks], ["1", "2", "3"])
        self.assertEqual([subtask.score for subtask in task.subtasks], [10, 20, 20])
        self.assertEqual(task.subtasks[2].depends_on, ["1", "2"])
        self.assertEqual(task.subtasks[1].members, [2, 3])
        self.assertEqual(task.remarks, [])


class KrsuEdgeCasesTest(ArchiveFixture):

    def read(self, manifest: str, extra_files: dict | None = None):
        files = {"testinfo.xml": manifest, **(extra_files or {})}
        return KrsuReader().read(ZipFileSource(self.pack(files)))

    def test_missing_manifest(self):
        with self.assertRaises(MalformedTask):
            KrsuReader().read(ZipFileSource(self.pack({"readme.txt": "x"})))

    def test_wrong_root_tag(self):
        with self.assertRaises(MalformedTask):
            self.read("<other/>")

    def test_broken_xml(self):
        with self.assertRaises(MalformedTask):
            self.read("<testinfo><timelimit>1000</testinfo>")

    def test_not_a_number(self):
        with self.assertRaises(MalformedTask):
            self.read("<testinfo><timelimit>abc</timelimit></testinfo>")

    def test_empty_tags_are_ignored(self):
        task = self.read("<testinfo><timelimit/><checker></checker></testinfo>")
        self.assertIsNone(task.cpu_ms)
        self.assertIsNone(task.verifier)

    def test_prereq_with_spaces_and_trailing_comma(self):
        task = self.read(
            '<testinfo><group id="1" points="1"/><group id="2" points="2"/>'
            '<group id="3" points="3" prereq=" 1 , 2, "/></testinfo>'
        )
        self.assertEqual(task.subtasks[2].depends_on, ["1", "2"])
        self.assertEqual(task.remarks, [])

    def test_unknown_group_and_missing_files_are_remarks(self):
        task = self.read(
            '<testinfo><group id="1" points="1" prereq="7"/>'
            '<test input="in.txt" output="out.txt" groupid="9"/></testinfo>',
            {"in.txt": "1"},
        )
        text = "\n".join(task.remarks)
        self.assertIn("несуществующую группу 9", text)
        self.assertIn("несуществующей группы 7", text)
        self.assertIn("нет файла out.txt", text)

    def test_manifest_in_nested_folder(self):
        path = self.pack({
            "task/sub/testinfo.xml": '<testinfo><test input="1.in" output="1.out"/></testinfo>',
            "task/sub/1.in": "",
            "task/sub/1.out": "",
            "task/other.txt": "",
        })
        task = KrsuReader().read(ZipFileSource(path))
        self.assertEqual(len(task.cases), 1)
        self.assertEqual(task.remarks, [])


if __name__ == "__main__":
    unittest.main()
