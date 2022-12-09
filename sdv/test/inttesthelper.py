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
import os
from typing import Dict, List, Mapping, Optional

import grpc

from sdv.proto.broker_pb2_grpc import BrokerStub
from sdv.proto.collector_pb2 import (
    RegisterDatapointsRequest,
    RegistrationMetadata,
    UpdateDatapointsRequest,
)
from sdv.proto.collector_pb2_grpc import CollectorStub
from sdv.proto.types_pb2 import ChangeType, Datapoint, DataType


class IntTestHelper:
    """IntTestHelper provides the Graph API to access the collector API of the
    Vehicle Data Broker."""

    def __init__(self, port: Optional[int] = None):
        if port is None:
            value = os.getenv("VDB_PORT")

            if value is not None:
                port = int(str(value))

        if port is None:
            port = 55555  # default port of Vehicle Data Broker when running locally

        self._address = f"localhost:{port}"
        self._channel = grpc.aio.insecure_channel(self._address)  # type: ignore
        self._collector_stub = CollectorStub(self._channel)
        self._broker_stub = BrokerStub(self._channel)

        self._ids: Dict[str, int] = None  # type: ignore

    async def close(self):
        """Closes runtime gRPC channel."""
        if self._channel:
            await self._channel.close()

    def __enter__(self) -> "IntTestHelper":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        asyncio.run_coroutine_threadsafe(self.close(), asyncio.get_event_loop())

    async def __register_datapoints(self, datapoints: list):
        response = await self._collector_stub.RegisterDatapoints(
            RegisterDatapointsRequest(list=datapoints)
        )

        return response

    async def __update_datapoints(self, datapoints: Mapping[int, Datapoint]):
        response = await self._collector_stub.UpdateDatapoints(
            UpdateDatapointsRequest(datapoints=datapoints)
        )

        return response

    async def __initialize_metadata(self):
        if self._ids is None:
            self._ids = {}
            response = await self._broker_stub.GetMetadata([])

            for item in response.list:
                self._ids[item.name] = item.id

    async def __get_or_create_datapoint_id_by_name(
        self, name: str, data_type: DataType
    ):
        await self.__initialize_metadata()

        key_list = self._ids.keys()
        if name not in key_list:
            response = await self.register_datapoint(name, data_type)
            datapoint_id = int(response)
            self._ids[name] = datapoint_id

        return self._ids[name]

    async def register_datapoint(self, name: str, data_type: DataType):
        await self.__initialize_metadata()

        registration_metadata = RegistrationMetadata()
        registration_metadata.name = name
        registration_metadata.data_type = data_type
        registration_metadata.description = ""
        registration_metadata.change_type = ChangeType.CONTINUOUS

        response = await self.__register_datapoints(datapoints=[registration_metadata])
        metadata_id = int(response.results[name])
        self._ids[name] = metadata_id
        return metadata_id

    async def set_bool_datapoint(self, name: str, value: bool):
        datapoint = Datapoint()
        datapoint.bool_value = value
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.BOOL  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_boolArray_datapoint(self, name: str, value: List[bool]):
        datapoint = Datapoint()
        for val in value:
            datapoint.bool_array.values.append(val)
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.BOOL_ARRAY  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_double_datapoint(self, name: str, value: float):
        datapoint = Datapoint()
        datapoint.double_value = value
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.DOUBLE  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_doubleArray_datapoint(self, name: str, value: List[float]):
        datapoint = Datapoint()
        for val in value:
            datapoint.double_array.values.append(val)
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.DOUBLE_ARRAY  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_float_datapoint(self, name: str, value: float):
        datapoint = Datapoint()
        datapoint.float_value = value
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.FLOAT  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_floatArray_datapoint(self, name: str, value: List[float]):
        datapoint = Datapoint()
        for val in value:
            datapoint.float_array.values.append(val)
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.FLOAT_ARRAY  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_int8_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.int32_value = value
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.INT32  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_int8Array_datapoint(self, name: str, value: List[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.int32_array.values.append(val)
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.INT32_ARRAY  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_int16_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.int32_value = value
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.INT32  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_int16Array_datapoint(self, name: str, value: List[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.int32_array.values.append(val)
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.INT32_ARRAY  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_int32_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.int32_value = value
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.INT32  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_int32Array_datapoint(self, name: str, value: List[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.int32_array.values.append(val)
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.INT32_ARRAY  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_int64_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.int64_value = value
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.INT64  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_int64Array_datapoint(self, name: str, value: List[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.int64_array.values.append(val)
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.INT64_ARRAY  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_string_datapoint(self, name: str, value: str):
        datapoint = Datapoint()
        datapoint.string_value = value
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.STRING  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_stringArray_datapoint(self, name: str, value: List[str]):
        datapoint = Datapoint()
        for val in value:
            datapoint.string_array.values.append(val)
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.STRING_ARRAY  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_uint8_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.uint32_value = value
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.UINT32  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_uint8Array_datapoint(self, name: str, value: List[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.uint32_array.values.append(val)
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.UINT32_ARRAY  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_uint16_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.uint32_value = value
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.UINT32  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_uint16Array_datapoint(self, name: str, value: List[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.uint32_array.values.append(val)
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.UINT32_ARRAY  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_uint32_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.uint32_value = value
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.UINT32  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_uint32Array_datapoint(self, name: str, value: List[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.uint32_array.values.append(val)
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.UINT32_ARRAY  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_uint64_datapoint(self, name: str, value: int):
        datapoint = Datapoint()
        datapoint.uint64_value = value
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.UINT64  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})

    async def set_uint64Array_datapoint(self, name: str, value: List[int]):
        datapoint = Datapoint()
        for val in value:
            datapoint.uint64_array.values.append(val)
        datapoint_id = await self.__get_or_create_datapoint_id_by_name(
            name, DataType.UINT64_ARRAY  # type: ignore
        )
        return await self.__update_datapoints({datapoint_id: datapoint})
