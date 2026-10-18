import sys

from app import ConsoleApp
from readers import standard_catalog
from report import TaskRenderer, TextReport
from storage import mount


def launch(argv: list[str] | None = None, renderer: TaskRenderer | None = None) -> int:
    app = ConsoleApp(
        catalog=standard_catalog(),
        opener=mount,
        renderer=renderer or TextReport(),
    )
    return app.run(argv)


if __name__ == "__main__":
    sys.exit(launch())
