from readers.catalog import ReaderCatalog
from readers.cats import CatsReader
from readers.contract import TaskReader
from readers.ejudge import EjudgeReader
from readers.krsu import KrsuReader


def standard_catalog() -> ReaderCatalog:
    catalog = ReaderCatalog()
    for reader in (KrsuReader(), CatsReader(), EjudgeReader()):
        catalog.enroll(reader)
    return catalog


__all__ = [
    "CatsReader",
    "EjudgeReader",
    "KrsuReader",
    "ReaderCatalog",
    "TaskReader",
    "standard_catalog",
]
