import xml.etree.ElementTree as ET

from domain import MalformedTask


def parse_tree(payload: bytes, label: str) -> ET.Element:
    try:
        return ET.fromstring(payload)
    except ET.ParseError as problem:
        raise MalformedTask(f"Некорректный XML в {label}: {problem}")


def inner_text(node: ET.Element, tag: str) -> str | None:
    child = node.find(tag)
    if child is None or child.text is None:
        return None
    return child.text.strip() or None
