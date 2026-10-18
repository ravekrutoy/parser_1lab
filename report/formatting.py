def describe_duration(ms: int | None) -> str | None:
    if ms is None:
        return None
    return f"{ms} мс ({ms / 1000:g} с)"


def describe_volume(byte_count: int | None) -> str | None:
    if byte_count is None:
        return None
    return f"{byte_count} байт ({byte_count / 1024 ** 2:g} МБ)"


def compress_ordinals(ordinals: list[int]) -> str:
    spans: list[list[int]] = []
    for ordinal in sorted(set(ordinals)):
        if spans and ordinal == spans[-1][1] + 1:
            spans[-1][1] = ordinal
        else:
            spans.append([ordinal, ordinal])
    return ", ".join(str(low) if low == high else f"{low}-{high}" for low, high in spans)
