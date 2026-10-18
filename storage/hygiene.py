from pathlib import PurePosixPath


def is_service_file(name: str) -> bool:
    return name.startswith("__MACOSX/") or PurePosixPath(name).name == ".DS_Store"


def wrapping_folder(names: list[str]) -> str:
    if not names or any("/" not in name for name in names):
        return ""
    tops = {name.split("/", 1)[0] for name in names}
    return tops.pop() + "/" if len(tops) == 1 else ""
