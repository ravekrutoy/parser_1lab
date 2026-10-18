from pathlib import Path

from storage.folder_source import FolderFileSource
from storage.source import FileSource
from storage.view import SourceView
from storage.zip_source import ZipFileSource


def mount(location: str) -> FileSource:
    if Path(location).is_dir():
        return FolderFileSource(location)
    return ZipFileSource(location)


__all__ = ["FileSource", "FolderFileSource", "SourceView", "ZipFileSource", "mount"]
