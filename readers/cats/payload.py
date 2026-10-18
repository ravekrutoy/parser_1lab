import xml.etree.ElementTree as ET


INLINE_MARK = "<"


def put_ordinal(template: str, ordinal: int) -> str:
    return template.replace("%0n", f"{ordinal:02d}").replace("%n", str(ordinal))


def describe_payload(node: ET.Element, ordinal: int, producer: str) -> str:
    file_name = node.get("src")
    if file_name:
        return put_ordinal(file_name, ordinal)

    program = node.get("use")
    if program:
        summary = f"{producer} '{program}'"
        arguments = node.get("param")
        if arguments:
            summary += f" {put_ordinal(arguments, ordinal)}"
        return f"{INLINE_MARK}{summary}>"

    return f"{INLINE_MARK}текст в XML>"


def names_a_file(payload: str | None) -> bool:
    return bool(payload) and not payload.startswith(INLINE_MARK)
