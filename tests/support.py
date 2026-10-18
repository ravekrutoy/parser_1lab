import tempfile
import unittest
import zipfile
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent
SAMPLES = PROJECT / "packages"


class ArchiveFixture(unittest.TestCase):

    def setUp(self):
        self._scratch = tempfile.TemporaryDirectory()
        self.scratch = Path(self._scratch.name)

    def tearDown(self):
        self._scratch.cleanup()

    def pack(self, files: dict[str, str | bytes], name: str = "package.zip") -> str:
        target = self.scratch / name
        with zipfile.ZipFile(target, "w") as archive:
            for member, content in files.items():
                archive.writestr(member, content)
        return str(target)
