# Copyright (c) 2022-2026 Contributors to the Eclipse Foundation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, overload

from velocitas_sdk.proto.types_pb2 import Datapoint as BrokerDatapoint
from velocitas_sdk.proto.val_pb2 import SubscribeResponse
from velocitas_sdk.vdb.types import TypedDataPointResult

if TYPE_CHECKING:
    from velocitas_sdk import model


class DataPointReply:
    """Wrapper for dynamic datatype casting of VDB reply."""

    def __init__(self):
        self.response = SubscribeResponse()

    def update(self, response: SubscribeResponse):
        self.response.MergeFrom(response)

    @overload
    def get(self, datapoint: model.DataPointBoolean) -> TypedDataPointResult[bool]: ...

    @overload
    def get(
        self, datapoint: model.DataPointBooleanArray
    ) -> TypedDataPointResult[list[bool]]: ...

    @overload
    def get(self, datapoint: model.DataPointDouble) -> TypedDataPointResult[float]: ...

    @overload
    def get(
        self, datapoint: model.DataPointDoubleArray
    ) -> TypedDataPointResult[list[float]]: ...

    @overload
    def get(self, datapoint: model.DataPointFloat) -> TypedDataPointResult[float]: ...

    @overload
    def get(
        self, datapoint: model.DataPointFloatArray
    ) -> TypedDataPointResult[list[float]]: ...

    @overload
    def get(self, datapoint: model.DataPointInt8) -> TypedDataPointResult[int]: ...

    @overload
    def get(
        self, datapoint: model.DataPointInt8Array
    ) -> TypedDataPointResult[list[int]]: ...

    @overload
    def get(self, datapoint: model.DataPointInt16) -> TypedDataPointResult[int]: ...

    @overload
    def get(
        self, datapoint: model.DataPointInt16Array
    ) -> TypedDataPointResult[list[int]]: ...

    @overload
    def get(self, datapoint: model.DataPointInt32) -> TypedDataPointResult[int]: ...

    @overload
    def get(
        self, datapoint: model.DataPointInt32Array
    ) -> TypedDataPointResult[list[int]]: ...

    @overload
    def get(self, datapoint: model.DataPointInt64) -> TypedDataPointResult[int]: ...

    @overload
    def get(
        self, datapoint: model.DataPointInt64Array
    ) -> TypedDataPointResult[list[int]]: ...

    @overload
    def get(self, datapoint: model.DataPointString) -> TypedDataPointResult[str]: ...

    @overload
    def get(
        self, datapoint: model.DataPointStringArray
    ) -> TypedDataPointResult[list[str]]: ...

    @overload
    def get(self, datapoint: model.DataPointUint8) -> TypedDataPointResult[int]: ...

    @overload
    def get(
        self, datapoint: model.DataPointUint8Array
    ) -> TypedDataPointResult[list[int]]: ...

    @overload
    def get(self, datapoint: model.DataPointUint16) -> TypedDataPointResult[int]: ...

    @overload
    def get(
        self, datapoint: model.DataPointUint16Array
    ) -> TypedDataPointResult[list[int]]: ...

    @overload
    def get(self, datapoint: model.DataPointUint32) -> TypedDataPointResult[int]: ...

    @overload
    def get(
        self, datapoint: model.DataPointUint32Array
    ) -> TypedDataPointResult[list[int]]: ...

    @overload
    def get(self, datapoint: model.DataPointUint64) -> TypedDataPointResult[int]: ...

    @overload
    def get(
        self, datapoint: model.DataPointUint64Array
    ) -> TypedDataPointResult[list[int]]: ...

    def get(self, datapoint: model.DataPoint):
        datapoint_type = datapoint.__class__.__name__
        vdb_datapoint: BrokerDatapoint | None = self.response.entries.get(
            datapoint.get_path()
        )
        if vdb_datapoint is None:
            raise Exception(
                f"Datapoint {datapoint.get_path()} not part of subscription"
            )
        datapoint_values = {
            "DataPointBoolean": vdb_datapoint.value.bool,
            "DataPointBooleanArray": list(vdb_datapoint.value.bool_array.values),
            "DataPointString": vdb_datapoint.value.string,
            "DataPointStringArray": list(vdb_datapoint.value.string_array.values),
            "DataPointDouble": vdb_datapoint.value.double,
            "DataPointDoubleArray": list(vdb_datapoint.value.double_array.values),
            "DataPointFloat": vdb_datapoint.value.float,
            "DataPointFloatArray": list(vdb_datapoint.value.float_array.values),
            "DataPointInt8": vdb_datapoint.value.int32,
            "DataPointInt8Array": list(vdb_datapoint.value.int32_array.values),
            "DataPointInt16": vdb_datapoint.value.int32,
            "DataPointInt16Array": list(vdb_datapoint.value.int32_array.values),
            "DataPointInt32": vdb_datapoint.value.int32,
            "DataPointInt32Array": list(vdb_datapoint.value.int32_array.values),
            "DataPointInt64": vdb_datapoint.value.int64,
            "DataPointInt64Array": list(vdb_datapoint.value.int64_array.values),
            "DataPointUint8": vdb_datapoint.value.uint32,
            "DataPointUint8Array": list(vdb_datapoint.value.uint32_array.values),
            "DataPointUint16": vdb_datapoint.value.uint32,
            "DataPointUint16Array": list(vdb_datapoint.value.uint32_array.values),
            "DataPointUint32": vdb_datapoint.value.uint32,
            "DataPointUint32Array": list(vdb_datapoint.value.uint32_array.values),
            "DataPointUint64": vdb_datapoint.value.uint64,
            "DataPointUint64Array": list(vdb_datapoint.value.uint64_array.values),
        }
        datapoint_value = datapoint_values.get(
            datapoint_type,
            Exception(f"Datapoint of type {datapoint_type} has an unknown value"),
        )

        if isinstance(datapoint_value, Exception):
            raise datapoint_value

        return TypedDataPointResult(
            datapoint.get_path(), datapoint_value, vdb_datapoint.timestamp
        )

    def signals(self):
        return self.response.entries.keys()
