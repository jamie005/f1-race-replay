from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class F1CarTelemeteryReport(_message.Message):
    __slots__ = ("query", "page_number", "results_per_page")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    RESULTS_PER_PAGE_FIELD_NUMBER: _ClassVar[int]
    query: str
    page_number: int
    results_per_page: int
    def __init__(self, query: _Optional[str] = ..., page_number: _Optional[int] = ..., results_per_page: _Optional[int] = ...) -> None: ...
