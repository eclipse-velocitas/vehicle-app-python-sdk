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

# pylint: disable=C0103

import asyncio
import contextvars
import logging
from typing import Generic, List, Type, TypeVar

import grpc
from deprecated import deprecated

from sdv.proto.types_pb2 import Datapoint as BrokerDatapoint
from sdv.vdb.client import VehicleDataBrokerClient
from sdv.vdb.subscriptions import SubscriptionManager, VdbSubscription

from . import conf

logger = logging.getLogger(__name__)

context = contextvars.ContextVar("context", default=[])  # type: ignore


class Context:
    """The Context for query assembly."""


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


class Model(Node):
    """The Model class represents a branch of the model tree, including root.
    Leafs are typcially one of the typed DataPoint* classes.
    But also a Model class can be a leaf, if it does not contain data Points, just methods."""


_COLLECTION_DEPRECATION_MSG = """The generated vehicle model must reflect the actual representation of the data points.
Please use base Model class instead."""


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


class Service(Node):
    """The Service class contains a set of gRPC methods"""

    def __init__(self):
        super().__init__()
        _address = conf.service_locator.get_location(self.name)
        self.channel = grpc.aio.insecure_channel(_address)  # type: ignore
        self.metadata = conf.service_locator.get_metadata(self.name)


class DataPoint(Node):
    """Base class for data points. Do not use for modelling directly."""

    def __init__(self, name: str, parent: Model):
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


class DataPointBoolean(DataPoint):
    """A data point with a value of type bool."""

    async def get(self) -> bool:
        try:
            response: BrokerDatapoint = await super().get()
            return response.bool_value
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointBool.get")
            logger.exception(ex)
            raise


class DataPointBooleanArray(DataPoint):
    """A data point array with a value of type boolean."""

    async def get(self) -> List[bool]:
        try:
            response: BrokerDatapoint = await super().get()
            return list(response.bool_array.values)
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointBoolArray.get")
            logger.exception(ex)
            raise


class DataPointInt8(DataPoint):
    """A data point with a value of type int32."""

    async def get(self) -> int:
        try:
            response: BrokerDatapoint = await super().get()
            return response.int32_value
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt8.get")
            logger.exception(ex)
            raise


class DataPointInt8Array(DataPoint):
    """A data point array with a value of type int32."""

    async def get(self) -> List[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return list(response.int32_array.values)
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt8Array.get")
            logger.exception(ex)
            raise


class DataPointInt16(DataPoint):
    """A data point with a value of type int32."""

    async def get(self) -> int:
        try:
            response: BrokerDatapoint = await super().get()
            return response.int32_value
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt16.get")
            logger.exception(ex)
            raise


class DataPointInt16Array(DataPoint):
    """A data point array with a value of type int32."""

    async def get(self) -> List[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return list(response.int32_array.values)
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt16Array.get")
            logger.exception(ex)
            raise


class DataPointInt32(DataPoint):
    """A data point with a value of type int32."""

    async def get(self) -> int:
        try:
            response: BrokerDatapoint = await super().get()
            return response.int32_value
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt32.get")
            logger.exception(ex)
            raise


class DataPointInt32Array(DataPoint):
    """A data point array with a value of type int32."""

    async def get(self) -> List[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return list(response.int32_array.values)
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt32Array.get")
            logger.exception(ex)
            raise


class DataPointInt64(DataPoint):
    """A data point with a value of type int64."""

    async def get(self) -> int:
        try:
            response: BrokerDatapoint = await super().get()
            return response.int64_value
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt64.get")
            logger.exception(ex)
            raise


class DataPointInt64Array(DataPoint):
    """A data point array with a value of type int64."""

    async def get(self) -> List[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return list(response.int64_array.values)
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointInt64Array.get")
            logger.exception(ex)
            raise


class DataPointUint8(DataPoint):
    """A data point with a value of type uint32."""

    async def get(self) -> int:
        try:
            response: BrokerDatapoint = await super().get()
            return response.uint32_value
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUInt8.get")
            logger.exception(ex)
            raise


class DataPointUint8Array(DataPoint):
    """A data point array with a value of type unsigned uint32."""

    async def get(self) -> List[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return list(response.uint32_array.values)
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUint8Array.get")
            logger.exception(ex)
            raise


class DataPointUint16(DataPoint):
    """A data point with a value of type uint32."""

    async def get(self) -> int:
        try:
            response: BrokerDatapoint = await super().get()
            return response.uint32_value
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUInt16.get")
            logger.exception(ex)
            raise


class DataPointUint16Array(DataPoint):
    """A data point array with a value of type unsigned uint32."""

    async def get(self) -> List[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return list(response.uint32_array.values)
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUint16Array.get")
            logger.exception(ex)
            raise


class DataPointUint32(DataPoint):
    """A data point with a value of type uint32."""

    async def get(self) -> int:
        try:
            response: BrokerDatapoint = await super().get()
            return response.uint32_value
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUInt32.get")
            logger.exception(ex)
            raise


class DataPointUint32Array(DataPoint):
    """A data point array with a value of type unsigned uint32."""

    async def get(self) -> List[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return list(response.uint32_array.values)
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUint32Array.get")
            logger.exception(ex)
            raise


class DataPointUint64(DataPoint):
    """A data point with a value of type unit64."""

    async def get(self) -> int:
        try:
            response: BrokerDatapoint = await super().get()
            return response.uint64_value
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUInt64.get")
            logger.exception(ex)
            raise


class DataPointUint64Array(DataPoint):
    """A data point array with a value of type unsigned uint64."""

    async def get(self) -> List[int]:
        try:
            response: BrokerDatapoint = await super().get()
            return list(response.uint64_array.values)
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointUint64Array.get")
            logger.exception(ex)
            raise


class DataPointFloat(DataPoint):
    """A data point with a value of type float."""

    async def get(self) -> float:
        try:
            response: BrokerDatapoint = await super().get()
            return response.float_value
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointFloat.get")
            logger.exception(ex)
            raise


class DataPointFloatArray(DataPoint):
    """A data point array with a value of type float."""

    async def get(self) -> List[float]:
        try:
            response: BrokerDatapoint = await super().get()
            return list(response.float_array.values)
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointFloatArray.get")
            logger.exception(ex)
            raise


class DataPointDouble(DataPoint):
    """A data point with a value of type double."""

    async def get(self) -> float:
        try:
            response: BrokerDatapoint = await super().get()
            return response.double_value
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointDouble.get")
            logger.exception(ex)
            raise


class DataPointDoubleArray(DataPoint):
    """A data point array with a value of type double."""

    async def get(self) -> List[float]:
        try:
            response: BrokerDatapoint = await super().get()
            return list(response.double_array.values)
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointDoubleArray.get")
            logger.exception(ex)
            raise


class DataPointString(DataPoint):
    """A data point with a value of type string."""

    async def get(self) -> str:
        try:
            response: BrokerDatapoint = await super().get()
            return response.string_value
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointString.get")
            logger.exception(ex)
            raise


class DataPointStringArray(DataPoint):
    """A data point array with a value of type String."""

    async def get(self) -> List[str]:
        try:
            response: BrokerDatapoint = await super().get()
            return list(response.string_array.values)
        except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
            logger.error("Error occured in DataPointStringArray.get")
            logger.exception(ex)
            raise
