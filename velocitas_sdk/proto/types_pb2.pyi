"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright (c) 2023-2024 Contributors to the Eclipse Foundation

This program and the accompanying materials are made available under the
terms of the Apache License, Version 2.0 which is available at
https://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.

SPDX-License-Identifier: Apache-2.0
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _DataType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _DataTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_DataType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    STRING: _DataType.ValueType  # 0
    BOOL: _DataType.ValueType  # 1
    INT8: _DataType.ValueType  # 2
    INT16: _DataType.ValueType  # 3
    INT32: _DataType.ValueType  # 4
    INT64: _DataType.ValueType  # 5
    UINT8: _DataType.ValueType  # 6
    UINT16: _DataType.ValueType  # 7
    UINT32: _DataType.ValueType  # 8
    UINT64: _DataType.ValueType  # 9
    FLOAT: _DataType.ValueType  # 10
    DOUBLE: _DataType.ValueType  # 11
    TIMESTAMP: _DataType.ValueType  # 12
    STRING_ARRAY: _DataType.ValueType  # 20
    BOOL_ARRAY: _DataType.ValueType  # 21
    INT8_ARRAY: _DataType.ValueType  # 22
    INT16_ARRAY: _DataType.ValueType  # 23
    INT32_ARRAY: _DataType.ValueType  # 24
    INT64_ARRAY: _DataType.ValueType  # 25
    UINT8_ARRAY: _DataType.ValueType  # 26
    UINT16_ARRAY: _DataType.ValueType  # 27
    UINT32_ARRAY: _DataType.ValueType  # 28
    UINT64_ARRAY: _DataType.ValueType  # 29
    FLOAT_ARRAY: _DataType.ValueType  # 30
    DOUBLE_ARRAY: _DataType.ValueType  # 31
    TIMESTAMP_ARRAY: _DataType.ValueType  # 32

class DataType(_DataType, metaclass=_DataTypeEnumTypeWrapper):
    """Data type of a signal

    Protobuf doesn't support int8, int16, uint8 or uint16.
    These are mapped to sint32 and uint32 respectively.
    """

STRING: DataType.ValueType  # 0
BOOL: DataType.ValueType  # 1
INT8: DataType.ValueType  # 2
INT16: DataType.ValueType  # 3
INT32: DataType.ValueType  # 4
INT64: DataType.ValueType  # 5
UINT8: DataType.ValueType  # 6
UINT16: DataType.ValueType  # 7
UINT32: DataType.ValueType  # 8
UINT64: DataType.ValueType  # 9
FLOAT: DataType.ValueType  # 10
DOUBLE: DataType.ValueType  # 11
TIMESTAMP: DataType.ValueType  # 12
STRING_ARRAY: DataType.ValueType  # 20
BOOL_ARRAY: DataType.ValueType  # 21
INT8_ARRAY: DataType.ValueType  # 22
INT16_ARRAY: DataType.ValueType  # 23
INT32_ARRAY: DataType.ValueType  # 24
INT64_ARRAY: DataType.ValueType  # 25
UINT8_ARRAY: DataType.ValueType  # 26
UINT16_ARRAY: DataType.ValueType  # 27
UINT32_ARRAY: DataType.ValueType  # 28
UINT64_ARRAY: DataType.ValueType  # 29
FLOAT_ARRAY: DataType.ValueType  # 30
DOUBLE_ARRAY: DataType.ValueType  # 31
TIMESTAMP_ARRAY: DataType.ValueType  # 32
global___DataType = DataType

class _DatapointError:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _DatapointErrorEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_DatapointError.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    UNKNOWN_DATAPOINT: _DatapointError.ValueType  # 0
    INVALID_TYPE: _DatapointError.ValueType  # 1
    ACCESS_DENIED: _DatapointError.ValueType  # 2
    INTERNAL_ERROR: _DatapointError.ValueType  # 3
    OUT_OF_BOUNDS: _DatapointError.ValueType  # 4

class DatapointError(_DatapointError, metaclass=_DatapointErrorEnumTypeWrapper): ...

UNKNOWN_DATAPOINT: DatapointError.ValueType  # 0
INVALID_TYPE: DatapointError.ValueType  # 1
ACCESS_DENIED: DatapointError.ValueType  # 2
INTERNAL_ERROR: DatapointError.ValueType  # 3
OUT_OF_BOUNDS: DatapointError.ValueType  # 4
global___DatapointError = DatapointError

class _ChangeType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _ChangeTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ChangeType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    STATIC: _ChangeType.ValueType  # 0
    """Value never changes"""
    ON_CHANGE: _ChangeType.ValueType  # 1
    """Updates are provided every time the value changes (i.e."""
    CONTINUOUS: _ChangeType.ValueType  # 2
    """window is open / closed)
    Value is updated continuously. Broker needs to tell
    """

class ChangeType(_ChangeType, metaclass=_ChangeTypeEnumTypeWrapper): ...

STATIC: ChangeType.ValueType  # 0
"""Value never changes"""
ON_CHANGE: ChangeType.ValueType  # 1
"""Updates are provided every time the value changes (i.e."""
CONTINUOUS: ChangeType.ValueType  # 2
"""window is open / closed)
Value is updated continuously. Broker needs to tell
"""
global___ChangeType = ChangeType

@typing_extensions.final
class StringArray(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["values", b"values"]) -> None: ...

global___StringArray = StringArray

@typing_extensions.final
class BoolArray(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.bool]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.bool] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["values", b"values"]) -> None: ...

global___BoolArray = BoolArray

@typing_extensions.final
class Int32Array(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["values", b"values"]) -> None: ...

global___Int32Array = Int32Array

@typing_extensions.final
class Int64Array(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["values", b"values"]) -> None: ...

global___Int64Array = Int64Array

@typing_extensions.final
class Uint32Array(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["values", b"values"]) -> None: ...

global___Uint32Array = Uint32Array

@typing_extensions.final
class Uint64Array(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["values", b"values"]) -> None: ...

global___Uint64Array = Uint64Array

@typing_extensions.final
class FloatArray(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.float] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["values", b"values"]) -> None: ...

global___FloatArray = FloatArray

@typing_extensions.final
class DoubleArray(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.float] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["values", b"values"]) -> None: ...

global___DoubleArray = DoubleArray

@typing_extensions.final
class Datapoint(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Failure:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _FailureEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Datapoint._Failure.ValueType], builtins.type):  # noqa: F821
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        INVALID_VALUE: Datapoint._Failure.ValueType  # 0
        """The data point is known, but doesn't have a valid value"""
        NOT_AVAILABLE: Datapoint._Failure.ValueType  # 1
        """The data point is known, but no value is available"""
        UNKNOWN_DATAPOINT: Datapoint._Failure.ValueType  # 2
        """Unknown datapoint"""
        ACCESS_DENIED: Datapoint._Failure.ValueType  # 3
        """Access denied"""
        INTERNAL_ERROR: Datapoint._Failure.ValueType  # 4
        """Unexpected internal error"""

    class Failure(_Failure, metaclass=_FailureEnumTypeWrapper): ...
    INVALID_VALUE: Datapoint.Failure.ValueType  # 0
    """The data point is known, but doesn't have a valid value"""
    NOT_AVAILABLE: Datapoint.Failure.ValueType  # 1
    """The data point is known, but no value is available"""
    UNKNOWN_DATAPOINT: Datapoint.Failure.ValueType  # 2
    """Unknown datapoint"""
    ACCESS_DENIED: Datapoint.Failure.ValueType  # 3
    """Access denied"""
    INTERNAL_ERROR: Datapoint.Failure.ValueType  # 4
    """Unexpected internal error"""

    TIMESTAMP_FIELD_NUMBER: builtins.int
    FAILURE_VALUE_FIELD_NUMBER: builtins.int
    STRING_VALUE_FIELD_NUMBER: builtins.int
    BOOL_VALUE_FIELD_NUMBER: builtins.int
    INT32_VALUE_FIELD_NUMBER: builtins.int
    INT64_VALUE_FIELD_NUMBER: builtins.int
    UINT32_VALUE_FIELD_NUMBER: builtins.int
    UINT64_VALUE_FIELD_NUMBER: builtins.int
    FLOAT_VALUE_FIELD_NUMBER: builtins.int
    DOUBLE_VALUE_FIELD_NUMBER: builtins.int
    STRING_ARRAY_FIELD_NUMBER: builtins.int
    BOOL_ARRAY_FIELD_NUMBER: builtins.int
    INT32_ARRAY_FIELD_NUMBER: builtins.int
    INT64_ARRAY_FIELD_NUMBER: builtins.int
    UINT32_ARRAY_FIELD_NUMBER: builtins.int
    UINT64_ARRAY_FIELD_NUMBER: builtins.int
    FLOAT_ARRAY_FIELD_NUMBER: builtins.int
    DOUBLE_ARRAY_FIELD_NUMBER: builtins.int
    @property
    def timestamp(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Timestamp of the value"""
    failure_value: global___Datapoint.Failure.ValueType
    string_value: builtins.str
    bool_value: builtins.bool
    int32_value: builtins.int
    int64_value: builtins.int
    uint32_value: builtins.int
    uint64_value: builtins.int
    float_value: builtins.float
    double_value: builtins.float
    @property
    def string_array(self) -> global___StringArray: ...
    @property
    def bool_array(self) -> global___BoolArray: ...
    @property
    def int32_array(self) -> global___Int32Array: ...
    @property
    def int64_array(self) -> global___Int64Array: ...
    @property
    def uint32_array(self) -> global___Uint32Array: ...
    @property
    def uint64_array(self) -> global___Uint64Array: ...
    @property
    def float_array(self) -> global___FloatArray: ...
    @property
    def double_array(self) -> global___DoubleArray: ...
    def __init__(
        self,
        *,
        timestamp: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        failure_value: global___Datapoint.Failure.ValueType = ...,
        string_value: builtins.str = ...,
        bool_value: builtins.bool = ...,
        int32_value: builtins.int = ...,
        int64_value: builtins.int = ...,
        uint32_value: builtins.int = ...,
        uint64_value: builtins.int = ...,
        float_value: builtins.float = ...,
        double_value: builtins.float = ...,
        string_array: global___StringArray | None = ...,
        bool_array: global___BoolArray | None = ...,
        int32_array: global___Int32Array | None = ...,
        int64_array: global___Int64Array | None = ...,
        uint32_array: global___Uint32Array | None = ...,
        uint64_array: global___Uint64Array | None = ...,
        float_array: global___FloatArray | None = ...,
        double_array: global___DoubleArray | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["bool_array", b"bool_array", "bool_value", b"bool_value", "double_array", b"double_array", "double_value", b"double_value", "failure_value", b"failure_value", "float_array", b"float_array", "float_value", b"float_value", "int32_array", b"int32_array", "int32_value", b"int32_value", "int64_array", b"int64_array", "int64_value", b"int64_value", "string_array", b"string_array", "string_value", b"string_value", "timestamp", b"timestamp", "uint32_array", b"uint32_array", "uint32_value", b"uint32_value", "uint64_array", b"uint64_array", "uint64_value", b"uint64_value", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["bool_array", b"bool_array", "bool_value", b"bool_value", "double_array", b"double_array", "double_value", b"double_value", "failure_value", b"failure_value", "float_array", b"float_array", "float_value", b"float_value", "int32_array", b"int32_array", "int32_value", b"int32_value", "int64_array", b"int64_array", "int64_value", b"int64_value", "string_array", b"string_array", "string_value", b"string_value", "timestamp", b"timestamp", "uint32_array", b"uint32_array", "uint32_value", b"uint32_value", "uint64_array", b"uint64_array", "uint64_value", b"uint64_value", "value", b"value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["value", b"value"]) -> typing_extensions.Literal["failure_value", "string_value", "bool_value", "int32_value", "int64_value", "uint32_value", "uint64_value", "float_value", "double_value", "string_array", "bool_array", "int32_array", "int64_array", "uint32_array", "uint64_array", "float_array", "double_array"] | None: ...

global___Datapoint = Datapoint

@typing_extensions.final
class Metadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DATA_TYPE_FIELD_NUMBER: builtins.int
    CHANGE_TYPE_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    id: builtins.int
    """Id to be used in "get" and "subscribe" requests. Ids stay valid during
    one power cycle, only.
    """
    name: builtins.str
    data_type: global___DataType.ValueType
    change_type: global___ChangeType.ValueType
    """CONTINUOUS or STATIC or ON_CHANGE"""
    description: builtins.str
    def __init__(
        self,
        *,
        id: builtins.int = ...,
        name: builtins.str = ...,
        data_type: global___DataType.ValueType = ...,
        change_type: global___ChangeType.ValueType = ...,
        description: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["change_type", b"change_type", "data_type", b"data_type", "description", b"description", "id", b"id", "name", b"name"]) -> None: ...

global___Metadata = Metadata
