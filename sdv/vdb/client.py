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
import logging
from typing import List, Optional
from urllib.parse import urlparse

import grpc

from sdv import config
import sdv.proto.val_pb2 as val
import sdv.proto.types_pb2 as types
from sdv.proto.val_pb2_grpc import VALStub

logger = logging.getLogger(__name__)


class VehicleDataBrokerClient:
    """VehicleDataBrokerClient provides the Graph API to access vehicle services
    and vehicle signals."""

    _instance = None

    def __new__(cls, port: Optional[int] = None):
        if cls._instance is None:
            cls._instance = super(VehicleDataBrokerClient, cls).__new__(cls)
            service_locator = config.middleware.service_locator
            _location = service_locator.get_service_location("vehicledatabroker")
            _hostname = urlparse(_location).hostname
            if port is None:
                _port = urlparse(_location).port
            else:
                _port = port

            _address = f"{_hostname}:{_port}"
            cls._channel = grpc.aio.insecure_channel(_address)  # type: ignore

            metadata = service_locator.get_metadata("vehicledatabroker")
            cls._metadata = metadata

            cls._stub = VALStub(cls._channel)
        return cls._instance

    async def close(self):
        """Closes runtime gRPC channel."""
        if self._channel:
            await self._channel.close()

    def __enter__(self) -> "VehicleDataBrokerClient":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        asyncio.run_coroutine_threadsafe(self.close(), asyncio.get_event_loop())

    async def GetDatapoints(self, datapoints: List[str]):
        entries = (
            val.EntryRequest(
                path=point,
                fields=(types.FIELD_UNSPECIFIED,),
                view=types.VIEW_CURRENT_VALUE,
            )
            for point in datapoints
        )
        try:
            response = await self._stub.Get(
                val.GetRequest(entries=entries), metadata=self._metadata
            )
            return response
        except grpc.aio.AioRpcError:  # type: ignore
            logger.exception(
                "Error occured in VehicleDataBrokerClient.GetDatapoints",
            )
            raise

    async def SetDatapoints(self, datapoints: dict):
        updates = (
            val.EntryUpdate(
                entry=types.DataEntry(path=key, value=datapoints[key]),
                fields=(types.FIELD_ACTUATOR_TARGET,),
            )
            for key in datapoints.keys()
        )

        try:
            response = await self._stub.Set(
                val.SetRequest(updates=updates),
                metadata=self._metadata,
            )
            return response
        except grpc.aio.AioRpcError:  # type: ignore
            logger.exception(
                "Error occured in VehicleDataBrokerClient.SetDatapoints",
            )
            raise

    def Subscribe(self, path: str):
        try:
            response = self._stub.Subscribe(
                val.SubscribeRequest(
                    entries=(
                        val.SubscribeEntry(
                            path=path,
                            fields=(types.FIELD_VALUE,),
                            view=types.VIEW_CURRENT_VALUE,
                        ),
                    )
                ),
                metadata=self._metadata,
            )
            return response
        except grpc.aio.AioRpcError:  # type: ignore
            logger.exception(
                "Error occured in VehicleDataBrokerClient.Subscribe",
            )
            raise

    async def GetMetadata(self, names: list):
        try:
            response = await self._stub.GetServerInfo(
                val.GetServerInfoRequest(), metadata=self._metadata
            )
            return response
        except grpc.aio.AioRpcError:  # type: ignore
            logger.exception(
                "Error occured in VehicleDataBrokerClient.GetMetadata",
            )
            raise
