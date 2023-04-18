from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DATA_TYPE_BOOLEAN: DataType
DATA_TYPE_BOOLEAN_ARRAY: DataType
DATA_TYPE_DOUBLE: DataType
DATA_TYPE_DOUBLE_ARRAY: DataType
DATA_TYPE_FLOAT: DataType
DATA_TYPE_FLOAT_ARRAY: DataType
DATA_TYPE_INT16: DataType
DATA_TYPE_INT16_ARRAY: DataType
DATA_TYPE_INT32: DataType
DATA_TYPE_INT32_ARRAY: DataType
DATA_TYPE_INT64: DataType
DATA_TYPE_INT64_ARRAY: DataType
DATA_TYPE_INT8: DataType
DATA_TYPE_INT8_ARRAY: DataType
DATA_TYPE_STRING: DataType
DATA_TYPE_STRING_ARRAY: DataType
DATA_TYPE_TIMESTAMP: DataType
DATA_TYPE_TIMESTAMP_ARRAY: DataType
DATA_TYPE_UINT16: DataType
DATA_TYPE_UINT16_ARRAY: DataType
DATA_TYPE_UINT32: DataType
DATA_TYPE_UINT32_ARRAY: DataType
DATA_TYPE_UINT64: DataType
DATA_TYPE_UINT64_ARRAY: DataType
DATA_TYPE_UINT8: DataType
DATA_TYPE_UINT8_ARRAY: DataType
DATA_TYPE_UNSPECIFIED: DataType
DESCRIPTOR: _descriptor.FileDescriptor
ENTRY_TYPE_ACTUATOR: EntryType
ENTRY_TYPE_ATTRIBUTE: EntryType
ENTRY_TYPE_SENSOR: EntryType
ENTRY_TYPE_UNSPECIFIED: EntryType
FIELD_ACTUATOR_TARGET: Field
FIELD_METADATA: Field
FIELD_METADATA_ACTUATOR: Field
FIELD_METADATA_ATTRIBUTE: Field
FIELD_METADATA_COMMENT: Field
FIELD_METADATA_DATA_TYPE: Field
FIELD_METADATA_DEPRECATION: Field
FIELD_METADATA_DESCRIPTION: Field
FIELD_METADATA_ENTRY_TYPE: Field
FIELD_METADATA_SENSOR: Field
FIELD_METADATA_UNIT: Field
FIELD_METADATA_VALUE_RESTRICTION: Field
FIELD_PATH: Field
FIELD_UNSPECIFIED: Field
FIELD_VALUE: Field
VIEW_ALL: View
VIEW_CURRENT_VALUE: View
VIEW_FIELDS: View
VIEW_METADATA: View
VIEW_TARGET_VALUE: View
VIEW_UNSPECIFIED: View

class Actuator(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Attribute(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class BoolArray(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, values: _Optional[_Iterable[bool]] = ...) -> None: ...

class DataEntry(_message.Message):
    __slots__ = ["actuator_target", "metadata", "path", "value"]
    ACTUATOR_TARGET_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    actuator_target: Datapoint
    metadata: Metadata
    path: str
    value: Datapoint
    def __init__(self, path: _Optional[str] = ..., value: _Optional[_Union[Datapoint, _Mapping]] = ..., actuator_target: _Optional[_Union[Datapoint, _Mapping]] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ...) -> None: ...

class DataEntryError(_message.Message):
    __slots__ = ["error", "path"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    error: Error
    path: str
    def __init__(self, path: _Optional[str] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class Datapoint(_message.Message):
    __slots__ = ["bool", "bool_array", "double", "double_array", "float", "float_array", "int32", "int32_array", "int64", "int64_array", "string", "string_array", "timestamp", "uint32", "uint32_array", "uint64", "uint64_array"]
    BOOL_ARRAY_FIELD_NUMBER: _ClassVar[int]
    BOOL_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_ARRAY_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_ARRAY_FIELD_NUMBER: _ClassVar[int]
    FLOAT_FIELD_NUMBER: _ClassVar[int]
    INT32_ARRAY_FIELD_NUMBER: _ClassVar[int]
    INT32_FIELD_NUMBER: _ClassVar[int]
    INT64_ARRAY_FIELD_NUMBER: _ClassVar[int]
    INT64_FIELD_NUMBER: _ClassVar[int]
    STRING_ARRAY_FIELD_NUMBER: _ClassVar[int]
    STRING_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UINT32_ARRAY_FIELD_NUMBER: _ClassVar[int]
    UINT32_FIELD_NUMBER: _ClassVar[int]
    UINT64_ARRAY_FIELD_NUMBER: _ClassVar[int]
    UINT64_FIELD_NUMBER: _ClassVar[int]
    bool: bool
    bool_array: BoolArray
    double: float
    double_array: DoubleArray
    float: float
    float_array: FloatArray
    int32: int
    int32_array: Int32Array
    int64: int
    int64_array: Int64Array
    string: str
    string_array: StringArray
    timestamp: _timestamp_pb2.Timestamp
    uint32: int
    uint32_array: Uint32Array
    uint64: int
    uint64_array: Uint64Array
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., string: _Optional[str] = ..., bool: bool = ..., int32: _Optional[int] = ..., int64: _Optional[int] = ..., uint32: _Optional[int] = ..., uint64: _Optional[int] = ..., float: _Optional[float] = ..., double: _Optional[float] = ..., string_array: _Optional[_Union[StringArray, _Mapping]] = ..., bool_array: _Optional[_Union[BoolArray, _Mapping]] = ..., int32_array: _Optional[_Union[Int32Array, _Mapping]] = ..., int64_array: _Optional[_Union[Int64Array, _Mapping]] = ..., uint32_array: _Optional[_Union[Uint32Array, _Mapping]] = ..., uint64_array: _Optional[_Union[Uint64Array, _Mapping]] = ..., float_array: _Optional[_Union[FloatArray, _Mapping]] = ..., double_array: _Optional[_Union[DoubleArray, _Mapping]] = ...) -> None: ...

class DoubleArray(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, values: _Optional[_Iterable[float]] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ["code", "message", "reason"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    reason: str
    def __init__(self, code: _Optional[int] = ..., reason: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class FloatArray(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, values: _Optional[_Iterable[float]] = ...) -> None: ...

class Int32Array(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class Int64Array(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ["actuator", "attribute", "comment", "data_type", "deprecation", "description", "entry_type", "sensor", "unit", "value_restriction"]
    ACTUATOR_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEPRECATION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENTRY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    VALUE_RESTRICTION_FIELD_NUMBER: _ClassVar[int]
    actuator: Actuator
    attribute: Attribute
    comment: str
    data_type: DataType
    deprecation: str
    description: str
    entry_type: EntryType
    sensor: Sensor
    unit: str
    value_restriction: ValueRestriction
    def __init__(self, data_type: _Optional[_Union[DataType, str]] = ..., entry_type: _Optional[_Union[EntryType, str]] = ..., description: _Optional[str] = ..., comment: _Optional[str] = ..., deprecation: _Optional[str] = ..., unit: _Optional[str] = ..., value_restriction: _Optional[_Union[ValueRestriction, _Mapping]] = ..., actuator: _Optional[_Union[Actuator, _Mapping]] = ..., sensor: _Optional[_Union[Sensor, _Mapping]] = ..., attribute: _Optional[_Union[Attribute, _Mapping]] = ...) -> None: ...

class Sensor(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class StringArray(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class Uint32Array(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class Uint64Array(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, values: _Optional[_Iterable[int]] = ...) -> None: ...

class ValueRestriction(_message.Message):
    __slots__ = ["floating_point", "signed", "string", "unsigned"]
    FLOATING_POINT_FIELD_NUMBER: _ClassVar[int]
    SIGNED_FIELD_NUMBER: _ClassVar[int]
    STRING_FIELD_NUMBER: _ClassVar[int]
    UNSIGNED_FIELD_NUMBER: _ClassVar[int]
    floating_point: ValueRestrictionFloat
    signed: ValueRestrictionInt
    string: ValueRestrictionString
    unsigned: ValueRestrictionUint
    def __init__(self, string: _Optional[_Union[ValueRestrictionString, _Mapping]] = ..., signed: _Optional[_Union[ValueRestrictionInt, _Mapping]] = ..., unsigned: _Optional[_Union[ValueRestrictionUint, _Mapping]] = ..., floating_point: _Optional[_Union[ValueRestrictionFloat, _Mapping]] = ...) -> None: ...

class ValueRestrictionFloat(_message.Message):
    __slots__ = ["allowed_values", "max", "min"]
    ALLOWED_VALUES_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    allowed_values: _containers.RepeatedScalarFieldContainer[float]
    max: float
    min: float
    def __init__(self, min: _Optional[float] = ..., max: _Optional[float] = ..., allowed_values: _Optional[_Iterable[float]] = ...) -> None: ...

class ValueRestrictionInt(_message.Message):
    __slots__ = ["allowed_values", "max", "min"]
    ALLOWED_VALUES_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    allowed_values: _containers.RepeatedScalarFieldContainer[int]
    max: int
    min: int
    def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ..., allowed_values: _Optional[_Iterable[int]] = ...) -> None: ...

class ValueRestrictionString(_message.Message):
    __slots__ = ["allowed_values"]
    ALLOWED_VALUES_FIELD_NUMBER: _ClassVar[int]
    allowed_values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, allowed_values: _Optional[_Iterable[str]] = ...) -> None: ...

class ValueRestrictionUint(_message.Message):
    __slots__ = ["allowed_values", "max", "min"]
    ALLOWED_VALUES_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    allowed_values: _containers.RepeatedScalarFieldContainer[int]
    max: int
    min: int
    def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ..., allowed_values: _Optional[_Iterable[int]] = ...) -> None: ...

class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class EntryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class View(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Field(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
