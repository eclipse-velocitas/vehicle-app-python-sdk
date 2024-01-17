"""
@generated by mypy-protobuf.  Do not edit manually!
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _AcStatus:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _AcStatusEnumTypeWrapper(
    google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_AcStatus.ValueType],
    builtins.type,
):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    OFF: _AcStatus.ValueType  # 0
    ON: _AcStatus.ValueType  # 1

class AcStatus(_AcStatus, metaclass=_AcStatusEnumTypeWrapper):
    pass

OFF: AcStatus.ValueType  # 0
ON: AcStatus.ValueType  # 1
global___AcStatus = AcStatus

class SetAcStatusRequest(google.protobuf.message.Message):
    """*
    @brief
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    STATUS_FIELD_NUMBER: builtins.int
    status: global___AcStatus.ValueType
    """The desired status of A/C"""

    def __init__(
        self,
        *,
        status: global___AcStatus.ValueType = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["status", b"status"]
    ) -> None: ...

global___SetAcStatusRequest = SetAcStatusRequest

class SetAcStatusReply(google.protobuf.message.Message):
    """*
    @brief
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    def __init__(
        self,
    ) -> None: ...

global___SetAcStatusReply = SetAcStatusReply

class SetTemperatureRequest(google.protobuf.message.Message):
    """*
    @brief
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TEMPERATURE_FIELD_NUMBER: builtins.int
    temperature: builtins.float
    """The desired cabin temperature in degree Celsius"""

    def __init__(
        self,
        *,
        temperature: builtins.float = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["temperature", b"temperature"]
    ) -> None: ...

global___SetTemperatureRequest = SetTemperatureRequest

class SetTemperatureReply(google.protobuf.message.Message):
    """*
    @brief
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    def __init__(
        self,
    ) -> None: ...

global___SetTemperatureReply = SetTemperatureReply
