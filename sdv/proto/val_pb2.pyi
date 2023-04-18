from sdv.proto import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class EntryRequest(_message.Message):
    __slots__ = ["fields", "path", "view"]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    VIEW_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedScalarFieldContainer[_types_pb2.Field]
    path: str
    view: _types_pb2.View
    def __init__(
        self,
        path: _Optional[str] = ...,
        view: _Optional[_Union[_types_pb2.View, str]] = ...,
        fields: _Optional[_Iterable[_Union[_types_pb2.Field, str]]] = ...,
    ) -> None: ...

class EntryUpdate(_message.Message):
    __slots__ = ["entry", "fields"]
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    entry: _types_pb2.DataEntry
    fields: _containers.RepeatedScalarFieldContainer[_types_pb2.Field]
    def __init__(
        self,
        entry: _Optional[_Union[_types_pb2.DataEntry, _Mapping]] = ...,
        fields: _Optional[_Iterable[_Union[_types_pb2.Field, str]]] = ...,
    ) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ["entries"]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[EntryRequest]
    def __init__(
        self, entries: _Optional[_Iterable[_Union[EntryRequest, _Mapping]]] = ...
    ) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ["entries", "error", "errors"]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_types_pb2.DataEntry]
    error: _types_pb2.Error
    errors: _containers.RepeatedCompositeFieldContainer[_types_pb2.DataEntryError]
    def __init__(
        self,
        entries: _Optional[_Iterable[_Union[_types_pb2.DataEntry, _Mapping]]] = ...,
        errors: _Optional[_Iterable[_Union[_types_pb2.DataEntryError, _Mapping]]] = ...,
        error: _Optional[_Union[_types_pb2.Error, _Mapping]] = ...,
    ) -> None: ...

class GetServerInfoRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetServerInfoResponse(_message.Message):
    __slots__ = ["name", "version"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    def __init__(
        self, name: _Optional[str] = ..., version: _Optional[str] = ...
    ) -> None: ...

class SetRequest(_message.Message):
    __slots__ = ["updates"]
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    updates: _containers.RepeatedCompositeFieldContainer[EntryUpdate]
    def __init__(
        self, updates: _Optional[_Iterable[_Union[EntryUpdate, _Mapping]]] = ...
    ) -> None: ...

class SetResponse(_message.Message):
    __slots__ = ["error", "errors"]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: _types_pb2.Error
    errors: _containers.RepeatedCompositeFieldContainer[_types_pb2.DataEntryError]
    def __init__(
        self,
        error: _Optional[_Union[_types_pb2.Error, _Mapping]] = ...,
        errors: _Optional[_Iterable[_Union[_types_pb2.DataEntryError, _Mapping]]] = ...,
    ) -> None: ...

class SubscribeEntry(_message.Message):
    __slots__ = ["fields", "path", "view"]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    VIEW_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedScalarFieldContainer[_types_pb2.Field]
    path: str
    view: _types_pb2.View
    def __init__(
        self,
        path: _Optional[str] = ...,
        view: _Optional[_Union[_types_pb2.View, str]] = ...,
        fields: _Optional[_Iterable[_Union[_types_pb2.Field, str]]] = ...,
    ) -> None: ...

class SubscribeRequest(_message.Message):
    __slots__ = ["entries"]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[SubscribeEntry]
    def __init__(
        self, entries: _Optional[_Iterable[_Union[SubscribeEntry, _Mapping]]] = ...
    ) -> None: ...

class SubscribeResponse(_message.Message):
    __slots__ = ["updates"]
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    updates: _containers.RepeatedCompositeFieldContainer[EntryUpdate]
    def __init__(
        self, updates: _Optional[_Iterable[_Union[EntryUpdate, _Mapping]]] = ...
    ) -> None: ...
