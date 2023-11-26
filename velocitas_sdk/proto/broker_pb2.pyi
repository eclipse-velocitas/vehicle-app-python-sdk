"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright (c) 2022 Robert Bosch GmbH and Microsoft Corporation

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
import google.protobuf.message
import velocitas_sdk.proto.types_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class GetDatapointsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATAPOINTS_FIELD_NUMBER: builtins.int
    @property
    def datapoints(
        self,
    ) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """A list of requested data points."""
    def __init__(
        self,
        *,
        datapoints: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["datapoints", b"datapoints"]
    ) -> None: ...

global___GetDatapointsRequest = GetDatapointsRequest

@typing_extensions.final
class GetDatapointsReply(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class DatapointsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> sdv.databroker.v1.types_pb2.Datapoint: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: sdv.databroker.v1.types_pb2.Datapoint | None = ...,
        ) -> None: ...
        def HasField(
            self, field_name: typing_extensions.Literal["value", b"value"]
        ) -> builtins.bool: ...
        def ClearField(
            self,
            field_name: typing_extensions.Literal["key", b"key", "value", b"value"],
        ) -> None: ...

    DATAPOINTS_FIELD_NUMBER: builtins.int
    @property
    def datapoints(
        self,
    ) -> google.protobuf.internal.containers.MessageMap[
        builtins.str, sdv.databroker.v1.types_pb2.Datapoint
    ]:
        """Contains the values of the requested data points.
        If a requested data point is not available, the corresponding Datapoint
        will have the respective failure value set.
        """
    def __init__(
        self,
        *,
        datapoints: collections.abc.Mapping[
            builtins.str, sdv.databroker.v1.types_pb2.Datapoint
        ]
        | None = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["datapoints", b"datapoints"]
    ) -> None: ...

global___GetDatapointsReply = GetDatapointsReply

@typing_extensions.final
class SetDatapointsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class DatapointsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> sdv.databroker.v1.types_pb2.Datapoint: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: sdv.databroker.v1.types_pb2.Datapoint | None = ...,
        ) -> None: ...
        def HasField(
            self, field_name: typing_extensions.Literal["value", b"value"]
        ) -> builtins.bool: ...
        def ClearField(
            self,
            field_name: typing_extensions.Literal["key", b"key", "value", b"value"],
        ) -> None: ...

    DATAPOINTS_FIELD_NUMBER: builtins.int
    @property
    def datapoints(
        self,
    ) -> google.protobuf.internal.containers.MessageMap[
        builtins.str, sdv.databroker.v1.types_pb2.Datapoint
    ]:
        """A map of data points to set"""
    def __init__(
        self,
        *,
        datapoints: collections.abc.Mapping[
            builtins.str, sdv.databroker.v1.types_pb2.Datapoint
        ]
        | None = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["datapoints", b"datapoints"]
    ) -> None: ...

global___SetDatapointsRequest = SetDatapointsRequest

@typing_extensions.final
class SetDatapointsReply(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class ErrorsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: sdv.databroker.v1.types_pb2.DatapointError.ValueType
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: sdv.databroker.v1.types_pb2.DatapointError.ValueType = ...,
        ) -> None: ...
        def ClearField(
            self,
            field_name: typing_extensions.Literal["key", b"key", "value", b"value"],
        ) -> None: ...

    ERRORS_FIELD_NUMBER: builtins.int
    @property
    def errors(
        self,
    ) -> google.protobuf.internal.containers.ScalarMap[
        builtins.str, sdv.databroker.v1.types_pb2.DatapointError.ValueType
    ]:
        """A map of errors (if any)"""
    def __init__(
        self,
        *,
        errors: collections.abc.Mapping[
            builtins.str, sdv.databroker.v1.types_pb2.DatapointError.ValueType
        ]
        | None = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["errors", b"errors"]
    ) -> None: ...

global___SetDatapointsReply = SetDatapointsReply

@typing_extensions.final
class SubscribeRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    QUERY_FIELD_NUMBER: builtins.int
    query: builtins.str
    """Subscribe to a set of data points (or expressions) described
    by the provided query.
    The query syntax is a subset of SQL and is described in more
    detail in the QUERY.md file.
    """
    def __init__(
        self,
        *,
        query: builtins.str = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["query", b"query"]
    ) -> None: ...

global___SubscribeRequest = SubscribeRequest

@typing_extensions.final
class SubscribeReply(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class FieldsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> sdv.databroker.v1.types_pb2.Datapoint: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: sdv.databroker.v1.types_pb2.Datapoint | None = ...,
        ) -> None: ...
        def HasField(
            self, field_name: typing_extensions.Literal["value", b"value"]
        ) -> builtins.bool: ...
        def ClearField(
            self,
            field_name: typing_extensions.Literal["key", b"key", "value", b"value"],
        ) -> None: ...

    FIELDS_FIELD_NUMBER: builtins.int
    @property
    def fields(
        self,
    ) -> google.protobuf.internal.containers.MessageMap[
        builtins.str, sdv.databroker.v1.types_pb2.Datapoint
    ]:
        """Contains the fields specified by the query.
        If a requested data point value is not available, the corresponding
        Datapoint will have it's respective failure value set.
        """
    def __init__(
        self,
        *,
        fields: collections.abc.Mapping[
            builtins.str, sdv.databroker.v1.types_pb2.Datapoint
        ]
        | None = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["fields", b"fields"]
    ) -> None: ...

global___SubscribeReply = SubscribeReply

@typing_extensions.final
class GetMetadataRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMES_FIELD_NUMBER: builtins.int
    @property
    def names(
        self,
    ) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Request metadata for a list of data points referenced by their names.
        e.g. "Vehicle.Cabin.Seat.Row1.Pos1.Position" or "Vehicle.Speed".

        If no names are provided, metadata for all known data points will be
        returned.
        """
    def __init__(
        self,
        *,
        names: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["names", b"names"]
    ) -> None: ...

global___GetMetadataRequest = GetMetadataRequest

@typing_extensions.final
class GetMetadataReply(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LIST_FIELD_NUMBER: builtins.int
    @property
    def list(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        sdv.databroker.v1.types_pb2.Metadata
    ]:
        """Contains metadata of the requested data points. If a data point
        doesn't exist (i.e. not known to the Data Broker) the corresponding
        Metadata isn't part of the returned list.
        """
    def __init__(
        self,
        *,
        list: collections.abc.Iterable[sdv.databroker.v1.types_pb2.Metadata]
        | None = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["list", b"list"]
    ) -> None: ...

global___GetMetadataReply = GetMetadataReply
