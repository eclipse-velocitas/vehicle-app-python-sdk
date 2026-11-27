from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FilterError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FILTER_ERROR_CODE_UNSPECIFIED: _ClassVar[FilterError]
    FILTER_ERROR_CODE_UNKNOWN_SINGAL_ID: _ClassVar[FilterError]

class ProviderError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CODE_UNSPECIFIED: _ClassVar[ProviderError]
    CODE_NETWORK_ERROR: _ClassVar[ProviderError]
    CODE_OVERLOAD: _ClassVar[ProviderError]

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_CODE_UNSPECIFIED: _ClassVar[ErrorCode]
    ERROR_CODE_OK: _ClassVar[ErrorCode]
    ERROR_CODE_INVALID_ARGUMENT: _ClassVar[ErrorCode]
    ERROR_CODE_NOT_FOUND: _ClassVar[ErrorCode]
    ERROR_CODE_PERMISSION_DENIED: _ClassVar[ErrorCode]

class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATA_TYPE_UNSPECIFIED: _ClassVar[DataType]
    DATA_TYPE_STRING: _ClassVar[DataType]
    DATA_TYPE_BOOLEAN: _ClassVar[DataType]
    DATA_TYPE_INT8: _ClassVar[DataType]
    DATA_TYPE_INT16: _ClassVar[DataType]
    DATA_TYPE_INT32: _ClassVar[DataType]
    DATA_TYPE_INT64: _ClassVar[DataType]
    DATA_TYPE_UINT8: _ClassVar[DataType]
    DATA_TYPE_UINT16: _ClassVar[DataType]
    DATA_TYPE_UINT32: _ClassVar[DataType]
    DATA_TYPE_UINT64: _ClassVar[DataType]
    DATA_TYPE_FLOAT: _ClassVar[DataType]
    DATA_TYPE_DOUBLE: _ClassVar[DataType]
    DATA_TYPE_TIMESTAMP: _ClassVar[DataType]
    DATA_TYPE_STRING_ARRAY: _ClassVar[DataType]
    DATA_TYPE_BOOLEAN_ARRAY: _ClassVar[DataType]
    DATA_TYPE_INT8_ARRAY: _ClassVar[DataType]
    DATA_TYPE_INT16_ARRAY: _ClassVar[DataType]
    DATA_TYPE_INT32_ARRAY: _ClassVar[DataType]
    DATA_TYPE_INT64_ARRAY: _ClassVar[DataType]
    DATA_TYPE_UINT8_ARRAY: _ClassVar[DataType]
    DATA_TYPE_UINT16_ARRAY: _ClassVar[DataType]
    DATA_TYPE_UINT32_ARRAY: _ClassVar[DataType]
    DATA_TYPE_UINT64_ARRAY: _ClassVar[DataType]
    DATA_TYPE_FLOAT_ARRAY: _ClassVar[DataType]
    DATA_TYPE_DOUBLE_ARRAY: _ClassVar[DataType]
    DATA_TYPE_TIMESTAMP_ARRAY: _ClassVar[DataType]

class EntryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENTRY_TYPE_UNSPECIFIED: _ClassVar[EntryType]
    ENTRY_TYPE_ATTRIBUTE: _ClassVar[EntryType]
    ENTRY_TYPE_SENSOR: _ClassVar[EntryType]
    ENTRY_TYPE_ACTUATOR: _ClassVar[EntryType]
FILTER_ERROR_CODE_UNSPECIFIED: FilterError
FILTER_ERROR_CODE_UNKNOWN_SINGAL_ID: FilterError
CODE_UNSPECIFIED: ProviderError
CODE_NETWORK_ERROR: ProviderError
CODE_OVERLOAD: ProviderError
ERROR_CODE_UNSPECIFIED: ErrorCode
ERROR_CODE_OK: ErrorCode
ERROR_CODE_INVALID_ARGUMENT: ErrorCode
ERROR_CODE_NOT_FOUND: ErrorCode
ERROR_CODE_PERMISSION_DENIED: ErrorCode
DATA_TYPE_UNSPECIFIED: DataType
DATA_TYPE_STRING: DataType
DATA_TYPE_BOOLEAN: DataType
DATA_TYPE_INT8: DataType
DATA_TYPE_INT16: DataType
DATA_TYPE_INT32: DataType
DATA_TYPE_INT64: DataType
DATA_TYPE_UINT8: DataType
DATA_TYPE_UINT16: DataType
DATA_TYPE_UINT32: DataType
DATA_TYPE_UINT64: DataType
DATA_TYPE_FLOAT: DataType
DATA_TYPE_DOUBLE: DataType
DATA_TYPE_TIMESTAMP: DataType
DATA_TYPE_STRING_ARRAY: DataType
DATA_TYPE_BOOLEAN_ARRAY: DataType
DATA_TYPE_INT8_ARRAY: DataType
DATA_TYPE_INT16_ARRAY: DataType
DATA_TYPE_INT32_ARRAY: DataType
DATA_TYPE_INT64_ARRAY: DataType
DATA_TYPE_UINT8_ARRAY: DataType
DATA_TYPE_UINT16_ARRAY: DataType
DATA_TYPE_UINT32_ARRAY: DataType
DATA_TYPE_UINT64_ARRAY: DataType
DATA_TYPE_FLOAT_ARRAY: DataType
DATA_TYPE_DOUBLE_ARRAY: DataType
DATA_TYPE_TIMESTAMP_ARRAY: DataType
ENTRY_TYPE_UNSPECIFIED: EntryType
ENTRY_TYPE_ATTRIBUTE: EntryType
ENTRY_TYPE_SENSOR: EntryType
ENTRY_TYPE_ACTUATOR: EntryType

class Datapoint(_message.Message):
    __slots__ = ("timestamp", "value")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    value: Value
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., value: _Optional[_Union[Value, _Mapping]] = ...) -> None: ...

class Value(_message.Message):
    __slots__ = ("string", "bool", "int32", "int64", "uint32", "uint64", "float", "double", "string_array", "bool_array", "int32_array", "int64_array", "uint32_array", "uint64_array", "float_array", "double_array")
    STRING_FIELD_NUMBER: _ClassVar[int]
    BOOL_FIELD_NUMBER: _ClassVar[int]
    INT32_FIELD_NUMBER: _ClassVar[int]
    INT64_FIELD_NUMBER: _ClassVar[int]
    UINT32_FIELD_NUMBER: _ClassVar[int]
    UINT64_FIELD_NUMBER: _ClassVar[int]
    FLOAT_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    STRING_ARRAY_FIELD_NUMBER: _ClassVar[int]
    BOOL_ARRAY_FIELD_NUMBER: _ClassVar[int]
    INT32_ARRAY_FIELD_NUMBER: _ClassVar[int]
    INT64_ARRAY_FIELD_NUMBER: _ClassVar[int]
    UINT32_ARRAY_FIELD_NUMBER: _ClassVar[int]
    UINT64_ARRAY_FIELD_NUMBER: _ClassVar[int]
    FLOAT_ARRAY_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_ARRAY_FIELD_NUMBER: _ClassVar[int]
    string: str
    bool: bool
    int32: int
    int64: int
    uint32: int
    uint64: int
    float: float
    double: float
    string_array: StringArray
    bool_array: BoolArray
    int32_array: Int32Array
    int64_array: Int64Array
    uint32_array: Uint32Array
    uint64_array: Uint64Array
    float_array: FloatArray
    double_array: DoubleArray
    def __init__(self, string: _Optional[str] = ..., bool: bool = ..., int32: _Optional[int] = ..., int64: _Optional[int] = ..., uint32: _Optional[int] = ..., uint64: _Optional[int] = ..., float: _Optional[float] = ..., double: _Optional[float] = ..., string_array: _Optional[_Union[StringArray, _Mapping]] = ..., bool_array: _Optional[_Union[BoolArray, _Mapping]] = ..., int32_array: _Optional[_Union[Int32Array, _Mapping]] = ..., int64_array: _Optional[_Union[Int64Array, _Mapping]] = ..., uint32_array: _Optional[_Union[Uint32Array, _Mapping]] = ..., uint64_array: _Optional[_Union[Uint64Array, _Mapping]] = ..., float_array: _Optional[_Union[FloatArray, _Mapping]] = ..., double_array: _Optional[_Union[DoubleArray, _Mapping]] = ...) -> None: ...

class SampleInterval(_message.Message):
    __slots__ = ("interval_ms",)
    INTERVAL_MS_FIELD_NUMBER: _ClassVar[int]
    interval_ms: int
    def __init__(self, interval_ms: _Optional[int] = ...) -> None: ...

class Filter(_message.Message):
    __slots__ = ("duration_ms", "min_sample_interval")
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    MIN_SAMPLE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    duration_ms: int
    min_sample_interval: SampleInterval
    def __init__(self, duration_ms: _Optional[int] = ..., min_sample_interval: _Optional[_Union[SampleInterval, _Mapping]] = ...) -> None: ...

class SignalID(_message.Message):
    __slots__ = ("id", "path")
    ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    id: int
    path: str
    def __init__(self, id: _Optional[int] = ..., path: _Optional[str] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    message: str
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ..., message: _Optional[str] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ("path", "id", "data_type", "entry_type", "description", "comment", "deprecation", "unit", "allowed_values", "min", "max", "min_sample_interval")
    PATH_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENTRY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    DEPRECATION_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_VALUES_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MIN_SAMPLE_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    path: str
    id: int
    data_type: DataType
    entry_type: EntryType
    description: str
    comment: str
    deprecation: str
    unit: str
    allowed_values: Value
    min: Value
    max: Value
    min_sample_interval: SampleInterval
    def __init__(self, path: _Optional[str] = ..., id: _Optional[int] = ..., data_type: _Optional[_Union[DataType, str]] = ..., entry_type: _Optional[_Union[EntryType, str]] = ..., description: _Optional[str] = ..., comment: _Optional[str] = ..., deprecation: _Optional[str] = ..., unit: _Optional[str] = ..., allowed_values: _Optional[_Union[Value, _Mapping]] = ..., min: _Optional[_Union[Value, _Mapping]] = ..., max: _Optional[_Union[Value, _Mapping]] = ..., min_sample_interval: _Optional[_Union[SampleInterval, _Mapping]] = ...) -> None: ...

class StringArray(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class BoolArray(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, values: _Optional[_Iterable[bool]] = ...) -> None: ...

class Int32Array(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class Int64Array(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class Uint32Array(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class Uint64Array(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class FloatArray(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, values: _Optional[_Iterable[float]] = ...) -> None: ...

class DoubleArray(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, values: _Optional[_Iterable[float]] = ...) -> None: ...
