import unittest

from domain import SourceUnavailable, UnsupportedDialect
from readers import KrsuReader, standard_catalog
from report.formatting import compress_ordinals
from storage import SourceView, ZipFileSource
from tests.support import ArchiveFixture


class StorageTest(ArchiveFixture):

    def test_missing_file(self):
        with self.assertRaises(SourceUnavailable):
            ZipFileSource(str(self.scratch / "nope.zip"))

    def test_not_a_zip(self):
        fake = self.scratch / "fake.zip"
        fake.write_text("text")
        with self.assertRaises(SourceUnavailable):
            ZipFileSource(str(fake))

    def test_wrapping_folder_is_stripped(self):
        view = SourceView(ZipFileSource(self.pack({"task/a.xml": "", "task/t/1": "", "__MACOSX/x": ""})))
        self.assertEqual(view.entries(), ["a.xml", "t/1"])
        self.assertEqual(view.top_level(), ["a.xml"])

    def test_locate_prefers_shallow_paths(self):
        view = SourceView(ZipFileSource(self.pack({"a/b/X.cfg": "", "a/x.CFG": "", "y": ""})))
        self.assertEqual(view.locate("x.cfg"), ["a/x.CFG", "a/b/X.cfg"])


class CatalogTest(unittest.TestCase):

    def test_catalog(self):
        catalog = standard_catalog()
        self.assertEqual(catalog.dialects(), ["CATS", "EJUDGE", "KRSU"])
        self.assertIsInstance(catalog.pick("krsu"), KrsuReader)
        with self.assertRaises(UnsupportedDialect):
            catalog.pick("PCMS")


class FormattingTest(unittest.TestCase):

    def test_compress_ordinals(self):
        self.assertEqual(compress_ordinals([8, 1, 2, 3, 5, 7, 2]), "1-3, 5, 7-8")
        self.assertEqual(compress_ordinals([]), "")


if __name__ == "__main__":
    unittest.main()
