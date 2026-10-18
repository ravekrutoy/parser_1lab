class RejectedInput(Exception):
    pass


class SourceUnavailable(RejectedInput):
    pass


class MalformedTask(RejectedInput):
    pass


class UnsupportedDialect(RejectedInput):
    pass
