# Copyright (c) 2022-2023 Robert Bosch GmbH and Microsoft Corporation
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

# Copyright (c) 2022 Robert Bosch GmbH and Microsoft Corporation
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

import asyncio
import contextvars
import logging
from typing import Generic, List, Type, TypeVar, overload
from urllib.parse import urlparse

import grpc
from deprecated import deprecated

from sdv import config
from sdv.proto.types_pb2 import BoolArray
from sdv.proto.types_pb2 import Datapoint as BrokerDatapoint
from sdv.proto.types_pb2 import (
    DoubleArray,
    FloatArray,
    Int32Array,
    Int64Array,
    StringArray,
    Uint32Array,
    Uint64Array,
)
from sdv.vdb.client import VehicleDataBrokerClient
from sdv.vdb.subscriptions import SubscriptionManager, VdbSubscription
from sdv.vdb.types import TypedDataPointResult

logger = logging.getLogger(__name__)

context = contextvars.ContextVar("context", default=[])  # type: ignore


class Node:
    """Node in the tree structure."""

    def get_path(self):
        path = [self.name]
        node = self.parent
        while node:
            path.insert(0, node.name)
            node = node.parent

        return ".".join(path)

    def __init__(self, parent=None):
        self.name = type(self).__name__
        self.parent = parent

    def get_client(self):
        return VehicleDataBrokerClient()

    async def start(self):
        tasks = list(SubscriptionManager._subscription_tasks.values())
        await asyncio.gather(*tasks)

    def get_context(self) -> List[str]:
        return context.get()

    def set_context(self, ctx: List[str]):
        context.set(ctx)


class DataPoint(Node):
    """Base class for data points. Do not use for modelling directly."""

    def __init__(self, name: str, parent: Node):
        super().__init__(parent)
        self.name = name

    def join(self, *args):
        if not self.get_context():
            self.set_context([self.get_path()])

        for arg in args:
            self.get_context().append("JOIN")
            self.get_context().append(arg.get_path())

        return self

    def where(self, condition: str):
        if not self.get_context():
            self.set_context([self.get_path()])

        self.get_context().append("WHERE")
        self.get_context().append(condition)
        return self

    def get_query(self) -> str:
        if not self.get_context():
            self.set_context([self.get_path()])

        ctx = self.get_context()
        query = "SELECT " + " ".join(ctx).replace(" JOIN", ",")
        self.set_context([])
        return query

    async def subscribe(self, on_update):
        query = self.get_query()
        sub = VdbSubscription(self.get_client(), query, on_update)
        SubscriptionManager._add_subscription(sub)
        return sub

    async def get(self):
        try:
            path = self.get_path()
            response = await self.get_client().GetDatapoints([path])
            return response.datapoints[path]
        except (grpc.aio.AioRpcError, Exception):  # type: ignore
            logger.error("Error occured in DataPoint.get")
            logger.debug(
                "DataPoint.get: scope variable value at error -> {path: %s}",
                path,
            )
            raise

    async def set(self, value):
        """Override the data point setter for the target datapoint type.
        - An error will be raised if the target value can NOT be set successfully.
        """
        raise Exception(f"Unknown datpoint type for to set the value = {value}")

    async def _set(self, value, subclass_name: str):
        """Wrapper setter for the public set(value) with specific Datapoint type."""
        try:
            datapoint = self.create_broker_data_point(value)
            path = self.get_path()
            response = await self.get_client().SetDatapoints(
                datapoints={path: datapoint}
            )
            if response.errors:
                raise TypeError(
                    f"set target value for non-actuator {path} is not allowed!"
                )

        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in %s.set", subclass_name)
            logger.exception(ex)
            raise

    def create_broker_data_point(self, value):
        """Override the data point creator for the target datapoint type.
        - An error will be raised if the target value can NOT be set successfully.
        """
        raise Exception(f"Unsupported datpoint type for setting the value = {value}")


class DataPointBoolean(DataPoint):
    """A data point with a value of type bool."""

    async def get(self) -> TypedDataPointResult[bool]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[bool](
                self.get_path(), response.bool_value, response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointBoolean.get")
            logger.exception(ex)
            raise

    async def set(self, value: bool):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: bool):
        return BrokerDatapoint(bool_value=value)


class DataPointBooleanArray(DataPoint):
    """A data point array with a value of type boolean."""

    async def get(self) -> TypedDataPointResult[List[bool]]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[List[bool]](
                self.get_path(), list(response.bool_array.values), response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointBooleanArray.get")
            logger.exception(ex)
            raise

    async def set(self, value: List[bool]):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: List[bool]):
        array = BoolArray(values=value)
        return BrokerDatapoint(bool_array=array)


class DataPointInt8(DataPoint):
    """A data point with a value of type int32."""

    async def get(self) -> TypedDataPointResult[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[int](
                self.get_path(), response.int32_value, response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt8.get")
            logger.exception(ex)
            raise

    async def set(self, value: int):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: int):
        return BrokerDatapoint(int32_value=value)


class DataPointInt8Array(DataPoint):
    """A data point array with a value of type int32."""

    async def get(self) -> TypedDataPointResult[List[int]]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[List[int]](
                self.get_path(), list(response.int32_array.values), response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt8Array.get")
            logger.exception(ex)
            raise

    async def set(self, value: List[int]):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: List[int]):
        array = Int32Array(values=value)
        return BrokerDatapoint(int32_array=array)


class DataPointInt16(DataPoint):
    """A data point with a value of type int32."""

    async def get(self) -> TypedDataPointResult[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[int](
                self.get_path(), response.int32_value, response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt16.get")
            logger.exception(ex)
            raise

    async def set(self, value: int):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: int):
        return BrokerDatapoint(int32_value=value)


class DataPointInt16Array(DataPoint):
    """A data point array with a value of type int32."""

    async def get(self) -> TypedDataPointResult[List[int]]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[List[int]](
                self.get_path(), list(response.int32_array.values), response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt16Array.get")
            logger.exception(ex)
            raise

    async def set(self, value: List[int]):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: List[int]):
        array = Int32Array(values=value)
        return BrokerDatapoint(int32_array=array)


class DataPointInt32(DataPoint):
    """A data point with a value of type int32."""

    async def get(self) -> TypedDataPointResult[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[int](
                self.get_path(), response.int32_value, response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt32.get")
            logger.exception(ex)
            raise

    async def set(self, value: int):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: int):
        return BrokerDatapoint(int32_value=value)


class DataPointInt32Array(DataPoint):
    """A data point array with a value of type int32."""

    async def get(self) -> TypedDataPointResult[List[int]]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[List[int]](
                self.get_path(), list(response.int32_array.values), response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt32Array.get")
            logger.exception(ex)
            raise

    async def set(self, value: List[int]):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: List[int]):
        array = Int32Array(values=value)
        return BrokerDatapoint(int32_array=array)


class DataPointInt64(DataPoint):
    """A data point with a value of type int64."""

    async def get(self) -> TypedDataPointResult[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[int](
                self.get_path(), response.int64_value, response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt64.get")
            logger.exception(ex)
            raise

    async def set(self, value: int):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: int):
        return BrokerDatapoint(int64_value=value)


class DataPointInt64Array(DataPoint):
    """A data point array with a value of type int64."""

    async def get(self) -> TypedDataPointResult[List[int]]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[List[int]](
                self.get_path(), list(response.int64_array.values), response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt64Array.get")
            logger.exception(ex)
            raise

    async def set(self, value: List[int]):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: List[int]):
        array = Int64Array(values=value)
        return BrokerDatapoint(int64_array=array)


class DataPointUint8(DataPoint):
    """A data point with a value of type uint32."""

    async def get(self) -> TypedDataPointResult[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[int](
                self.get_path(), response.uint32_value, response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUInt8.get")
            logger.exception(ex)
            raise

    async def set(self, value: int):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: int):
        return BrokerDatapoint(uint32_value=value)


class DataPointUint8Array(DataPoint):
    """A data point array with a value of type unsigned uint32."""

    async def get(self) -> TypedDataPointResult[List[int]]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[List[int]](
                self.get_path(), list(response.uint32_array.values), response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUint8Array.get")
            logger.exception(ex)
            raise

    async def set(self, value: List[int]):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: List[int]):
        array = Uint32Array(values=value)
        return BrokerDatapoint(uint32_array=array)


class DataPointUint16(DataPoint):
    """A data point with a value of type uint32."""

    async def get(self) -> TypedDataPointResult[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[int](
                self.get_path(), response.uint32_value, response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUInt16.get")
            logger.exception(ex)
            raise

    async def set(self, value: int):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: int):
        return BrokerDatapoint(uint32_value=value)


class DataPointUint16Array(DataPoint):
    """A data point array with a value of type unsigned uint32."""

    async def get(self) -> TypedDataPointResult[List[int]]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[List[int]](
                self.get_path(), list(response.uint32_array.values), response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUint16Array.get")
            logger.exception(ex)
            raise

    async def set(self, value: List[int]):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: List[int]):
        array = Uint32Array(values=value)
        return BrokerDatapoint(uint32_array=array)


class DataPointUint32(DataPoint):
    """A data point with a value of type uint32."""

    async def get(self) -> TypedDataPointResult[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[int](
                self.get_path(), response.uint32_value, response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUInt32.get")
            logger.exception(ex)
            raise

    async def set(self, value: int):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: int):
        return BrokerDatapoint(uint32_value=value)


class DataPointUint32Array(DataPoint):
    """A data point array with a value of type unsigned uint32."""

    async def get(self) -> TypedDataPointResult[List[int]]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[List[int]](
                self.get_path(), list(response.uint32_array.values), response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUint32Array.get")
            logger.exception(ex)
            raise

    async def set(self, value: List[int]):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: List[int]):
        array = Uint32Array(values=value)
        return BrokerDatapoint(uint32_array=array)


class DataPointUint64(DataPoint):
    """A data point with a value of type unit64."""

    async def get(self) -> TypedDataPointResult[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[int](
                self.get_path(), response.uint64_value, response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUInt64.get")
            logger.exception(ex)
            raise

    async def set(self, value: int):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: int):
        return BrokerDatapoint(uint64_value=value)


class DataPointUint64Array(DataPoint):
    """A data point array with a value of type unsigned uint64."""

    async def get(self) -> TypedDataPointResult[List[int]]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[List[int]](
                self.get_path(), list(response.uint64_array.values), response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUint64Array.get")
            logger.exception(ex)
            raise

    async def set(self, value: List[int]):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: List[int]):
        array = Uint64Array(values=value)
        return BrokerDatapoint(uint64_array=array)


class DataPointFloat(DataPoint):
    """A data point with a value of type float."""

    async def get(self) -> TypedDataPointResult[float]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[float](
                self.get_path(), response.float_value, response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointFloat.get")
            logger.exception(ex)
            raise

    async def set(self, value: float):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: float):
        return BrokerDatapoint(float_value=value)


class DataPointFloatArray(DataPoint):
    """A data point array with a value of type float."""

    async def get(self) -> TypedDataPointResult[List[float]]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[List[float]](
                self.get_path(), list(response.float_array.values), response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointFloatArray.get")
            logger.exception(ex)
            raise

    async def set(self, value: List[float]):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: List[float]):
        array = FloatArray(values=value)
        return BrokerDatapoint(float_array=array)


class DataPointDouble(DataPoint):
    """A data point with a value of type double."""

    async def get(self) -> TypedDataPointResult[float]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[float](
                self.get_path(), response.double_value, response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointDouble.get")
            logger.exception(ex)
            raise

    async def set(self, value: float):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: float):
        return BrokerDatapoint(double_value=value)


class DataPointDoubleArray(DataPoint):
    """A data point array with a value of type double."""

    async def get(self) -> TypedDataPointResult[List[float]]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[List[float]](
                self.get_path(), list(response.double_array.values), response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointDoubleArray.get")
            logger.exception(ex)
            raise

    async def set(self, value: List[float]):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: List[float]):
        array = DoubleArray(values=value)
        return BrokerDatapoint(double_array=array)


class DataPointString(DataPoint):
    """A data point with a value of type string."""

    async def get(self) -> TypedDataPointResult[str]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[str](
                self.get_path(), response.string_value, response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointString.get")
            logger.exception(ex)
            raise

    async def set(self, value: str):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: str):
        return BrokerDatapoint(string_value=value)


class DataPointStringArray(DataPoint):
    """A data point array with a value of type String."""

    async def get(self) -> TypedDataPointResult[List[str]]:
        try:
            response: BrokerDatapoint = await super().get()
            return TypedDataPointResult[List[str]](
                self.get_path(), list(response.string_array.values), response.timestamp
            )
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointStringArray.get")
            logger.exception(ex)
            raise

    async def set(self, value: List[str]):
        await self._set(value, self.__class__.__name__)

    def create_broker_data_point(self, value: List[str]):
        array = StringArray(values=value)
        return BrokerDatapoint(string_array=array)


class BatchSetBuilder:
    """
    Collects data points to be set in a single 'atomic' operation.
    The data points to be set need being added in a chain of 'add' calls, which
    is terminated by an 'apply' call to commit the changed values to the data model:

    (
        await model.set_many()
        .add(model.subbranch.BoolDatapoint1, True)
        .add(model.subbranch.BoolDatapoint2, False)
        .apply()
    )
    """

    def __init__(self, client):
        self.__client = client
        self.__nodes = {}

    @overload
    def add(self, node: DataPointBoolean, value: bool) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointBooleanArray, value: List[bool]) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointDouble, value: float) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointDoubleArray, value: List[float]) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointFloat, value: float) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointFloatArray, value: List[float]) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointInt8, value: int) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointInt8Array, value: List[int]) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointInt16, value: int) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointInt16Array, value: List[int]) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointInt32, value: int) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointInt32Array, value: List[int]) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointInt64, value: int) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointInt64Array, value: List[int]) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointString, value: str) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointStringArray, value: List[str]) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointUint8, value: int) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointUint8Array, value: List[int]) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointUint16, value: int) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointUint16Array, value: List[int]) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointUint32, value: int) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointUint32Array, value: List[int]) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointUint64, value: int) -> "BatchSetBuilder":
        ...

    @overload
    def add(self, node: DataPointUint64Array, value: List[int]) -> "BatchSetBuilder":
        ...

    def add(self, node: DataPoint, value) -> "BatchSetBuilder":
        node_name = node.get_path()
        node_value = node.create_broker_data_point(value)
        if node_name in self.__nodes:
            logger.error(
                "Key '%s' already present in set-batch!"
                " Overwriting existing value '%s' with '%s'.",
                node_name,
                self.__nodes[node_name],
                node_value,
            )
        self.__nodes[node_name] = node_value
        return self

    async def apply(self):
        if len(self.__nodes) == 0:
            logger.warning("Empty node list, nothing updated")
            return

        try:
            response = await self.__client.SetDatapoints(self.__nodes)
            if response.errors:
                raise TypeError(
                    "Some data point values could not be set: ", response.errors
                )

        except (grpc.aio.AioRpcError, Exception):  # type: ignore
            logger.error("Error occured on updating several data points")
            raise


class Model(Node):
    """The Model class represents a branch of the model tree, including root.
    Leafs are typcially one of the typed DataPoint* classes.
    But also a Model class can be a leaf, if it does not contain data Points,
    just methods."""

    def set_many(self) -> BatchSetBuilder:
        return BatchSetBuilder(self.get_client())


class Service(Node):
    """The Service class contains a set of gRPC methods"""

    def __init__(self):
        super().__init__()
        service_locator = config.middleware.service_locator
        _location = service_locator.get_service_location(self.name)
        _hostname = urlparse(_location).hostname
        _port = urlparse(_location).port
        self.address = f"{_hostname}:{_port}"
        self.channel = grpc.aio.insecure_channel(self.address)  # type: ignore
        self.metadata = service_locator.get_metadata(self.name)


_COLLECTION_DEPRECATION_MSG = """The generated vehicle model must reflect the actual
representation of the data points. Please use base Model class instead."""


@deprecated(
    version="0.4.0",
    reason=_COLLECTION_DEPRECATION_MSG,
)
class ModelReferences:
    """ModelReferences class"""

    def to_string(self, selector) -> str:
        raise NotImplementedError()


@deprecated(
    version="0.4.0",
    reason=_COLLECTION_DEPRECATION_MSG,
)
class Dictionary(ModelReferences):
    """Dictionary class"""

    def __init__(self, list_type: Type):
        self.instances = []
        for i in list_type:
            self.instances.append(i)

    def to_string(self, selector) -> str:
        if selector not in self.instances:
            raise ValueError(f"{selector} is not in {self.instances}")

        return selector


@deprecated(
    version="0.4.0",
    reason=_COLLECTION_DEPRECATION_MSG,
)
class NamedRange(ModelReferences):
    """NamedRange class"""

    def __init__(self, name: str, start: int, end: int):
        self.start = start
        self.end = end
        self.name = name

    def to_string(self, selector: int) -> str:
        if (selector < self.start) or (selector > self.end):
            raise ValueError(f"{selector} is not in range {self.start}-{self.end}")

        return self.name + str(selector)


TModel = TypeVar("TModel", bound=Node)


@deprecated(
    version="0.4.0",
    reason=_COLLECTION_DEPRECATION_MSG,
)
class ModelCollection(Generic[TModel]):
    """ModelCollection class"""

    def __init__(self, model_refs: List[ModelReferences], model: Model):
        super().__init__()

        if model.parent is None:
            raise Exception(
                "ModelCollection require a parent, defining ModelInstances as root is \
                not allowed"
            )

        self.model = model
        self.specs = model_refs

    def element_at(self, *args) -> TModel:
        if len(args) != len(self.specs):
            raise Exception("Indexes length does not match specs length")

        segments = []
        for i, spec in enumerate(self.specs):
            selector = args[i]
            segment = spec.to_string(selector)
            segments.append(segment)

        path = self.model.__class__.__name__ + "." + ".".join(segments)

        # Modifying the original object may be problematic, better clone the object
        self.model.name = path
        return self.model  # type: ignore
