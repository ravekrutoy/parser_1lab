import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from main import launch
from report import TaskRenderer
from tests.support import SAMPLES


class ConsoleTest(unittest.TestCase):

    def run_app(self, *arguments, renderer=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = launch(list(arguments), renderer)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_krsu(self):
        code, out, _ = self.run_app("KRSU", str(SAMPLES / "krsu_A.zip"))
        self.assertEqual(code, 0)
        self.assertIn("ТЕСТЫ (27)", out)
        self.assertIn("Сумма баллов по тестам и группам: 100", out)
        self.assertNotIn("ПРЕДУПРЕЖДЕНИЯ", out)

    def test_ejudge(self):
        code, out, _ = self.run_app("ejudge", str(SAMPLES / "ejudge_sample.zip"))
        self.assertEqual(code, 0)
        self.assertIn("ТЕСТЫ (46)", out)
        self.assertIn("Сумма баллов по тестам и группам: 100", out)

    def test_cats(self):
        code, out, _ = self.run_app("cats", str(SAMPLES / "cats_area51.zip"))
        self.assertEqual(code, 0)
        self.assertIn("Название: Area 51", out)
        self.assertIn("ТЕСТЫ (42)", out)

    def test_custom_renderer(self):
        class CapturingRenderer(TaskRenderer):
            def render(self, task):
                self.task = task

        renderer = CapturingRenderer()
        code, out, _ = self.run_app("KRSU", str(SAMPLES / "krsu_A.zip"), renderer=renderer)
        self.assertEqual(code, 0)
        self.assertEqual(out, "")
        self.assertEqual(len(renderer.task.cases), 27)

    def test_errors_go_to_stderr(self):
        for arguments in (
            ("PCMS", str(SAMPLES / "krsu_A.zip")),
            ("KRSU", "nope.zip"),
            ("CATS", str(SAMPLES / "krsu_A.zip")),
            ("KRSU", str(SAMPLES / "cats_area51.zip")),
        ):
            with self.subTest(arguments=arguments):
                code, out, err = self.run_app(*arguments)
                self.assertEqual(code, 1)
                self.assertEqual(out, "")
                self.assertTrue(err.startswith("Ошибка:"))


if __name__ == "__main__":
    unittest.main()
