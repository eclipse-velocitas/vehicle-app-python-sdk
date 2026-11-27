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

import asyncio
import os

import grpc
from typing_extensions import Self

from velocitas_sdk.proto.types_pb2 import Datapoint, SignalID
from velocitas_sdk.proto.val_pb2 import PublishValueRequest
from velocitas_sdk.proto.val_pb2_grpc import VALStub


class IntTestHelper:
    """IntTestHelper provides the Graph API to access the collector API of the
    Vehicle Data Broker."""

    def __init__(self, port: int | None = None):
        if port is None:
            value = os.getenv("VDB_PORT")

            if value is not None:
                port = int(str(value))

        if port is None:
            port = 55555  # default port of Vehicle Data Broker when running locally

        self._address = f"localhost:{port}"
        self._channel = grpc.aio.insecure_channel(self._address)  # type: ignore
        self._broker_stub = VALStub(self._channel)

        self._ids: dict[str, int] = None  # type: ignore

    async def close(self):
        """Closes runtime gRPC channel."""
        if self._channel:
            await self._channel.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        asyncio.run_coroutine_threadsafe(self.close(), asyncio.get_event_loop())

    async def __update_datapoint(self, path, datapoint):
        await self._broker_stub.PublishValue(
            PublishValueRequest(signal_id=SignalID(path=path), data_point=datapoint)
        )

    async def set_bool_datapoint(self, name: str, value: bool):
        datapoint = Datapoint()
        datapoint.value.bool = value
        return await self.__update_datapoint(name, datapoint)

    async def set_boolArray_datapoint(self, name: str, value: list[bool]):
        datapoint = Datapoint()
        for val in value:
            datapoint.value.bool_array.values.append(val)
        return await self.__update_datapoint(name, datapoint)

    async def set_double_datapoint(self, name: str, value: float):
        datapoint = Datapoint()
        datapoint.value.double = value
        return await self.__update_datapoint(name, datapoint)

    async def set_doubleArray_datapoint(self, name: str, value: list[float]):
        datapoint = Datapoint()
        for val in value:
            datapoint.value.double_array.values.append(val)
        return await self.__update_datapoint(name, datapoint)

    async def set_float_datapoint(self, name: str, value: float):
        datapoint = Datapoint()
        datapoint.value.float = value
        return await self.__update_datapoint(name, datapoint)

    async def set_floatArray_datapoint(self, name: str, value: list[float]):
        datapoint = Datapoint()
        for val in value:
            datapoint.value.float_array.values.append(val)
        return await self.__update_datapoint(name, datapoint)

    async def set_int8_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.value.int32 = value
        return await self.__update_datapoint(name, datapoint)

    async def set_int8Array_datapoint(self, name: str, value: list[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.value.int32_array.values.append(val)
        return await self.__update_datapoint(name, datapoint)

    async def set_int16_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.value.int32 = value
        return await self.__update_datapoint(name, datapoint)

    async def set_int16Array_datapoint(self, name: str, value: list[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.value.int32_array.values.append(val)
        return await self.__update_datapoint(name, datapoint)

    async def set_int32_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.value.int32 = value
        return await self.__update_datapoint(name, datapoint)

    async def set_int32Array_datapoint(self, name: str, value: list[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.value.int32_array.values.append(val)
        return await self.__update_datapoint(name, datapoint)

    async def set_int64_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.value.int64 = value
        return await self.__update_datapoint(name, datapoint)

    async def set_int64Array_datapoint(self, name: str, value: list[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.value.int64_array.values.append(val)
        return await self.__update_datapoint(name, datapoint)

    async def set_string_datapoint(self, name: str, value: str):
        datapoint = Datapoint()
        datapoint.value.string = value
        return await self.__update_datapoint(name, datapoint)

    async def set_stringArray_datapoint(self, name: str, value: list[str]):
        datapoint = Datapoint()
        for val in value:
            datapoint.value.string_array.values.append(val)
        return await self.__update_datapoint(name, datapoint)

    async def set_uint8_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.value.uint32 = value
        return await self.__update_datapoint(name, datapoint)

    async def set_uint8Array_datapoint(self, name: str, value: list[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.value.uint32_array.values.append(val)
        return await self.__update_datapoint(name, datapoint)

    async def set_uint16_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.value.uint32 = value
        return await self.__update_datapoint(name, datapoint)

    async def set_uint16Array_datapoint(self, name: str, value: list[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.value.uint32_array.values.append(val)
        return await self.__update_datapoint(name, datapoint)

    async def set_uint32_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.value.uint32 = value
        return await self.__update_datapoint(name, datapoint)

    async def set_uint32Array_datapoint(self, name: str, value: list[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.value.uint32_array.values.append(val)
        return await self.__update_datapoint(name, datapoint)

    async def set_uint64_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.value.uint64 = value
        return await self.__update_datapoint(name, datapoint)

    async def set_uint64Array_datapoint(self, name: str, value: list[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.value.uint64_array.values.append(val)
        return await self.__update_datapoint(name, datapoint)
