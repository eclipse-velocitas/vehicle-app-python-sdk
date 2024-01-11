# Copyright (c) 2022-2024 Contributors to the Eclipse Foundation
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

from velocitas_sdk import config
from velocitas_sdk.proto.broker_pb2 import (
    GetDatapointsRequest,
    GetMetadataRequest,
    SetDatapointsRequest,
    SubscribeRequest,
)
from velocitas_sdk.proto.broker_pb2_grpc import BrokerStub

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

            cls._stub = BrokerStub(cls._channel)
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
        try:
            response = await self._stub.GetDatapoints(
                GetDatapointsRequest(datapoints=datapoints), metadata=self._metadata
            )
            return response
        except grpc.aio.AioRpcError:  # type: ignore
            logger.exception(
                "Error occured in VehicleDataBrokerClient.GetDatapoints",
            )
            raise

    async def SetDatapoints(self, datapoints):
        try:
            response = await self._stub.SetDatapoints(
                SetDatapointsRequest(datapoints=datapoints), metadata=self._metadata
            )
            return response
        except grpc.aio.AioRpcError:  # type: ignore
            logger.exception(
                "Error occured in VehicleDataBrokerClient.SetDatapoints",
            )
            raise

    def Subscribe(self, query: str):
        try:
            response = self._stub.Subscribe(
                SubscribeRequest(query=query),
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
            response = await self._stub.GetMetadata(
                GetMetadataRequest(names=names), metadata=self._metadata
            )
            return response
        except grpc.aio.AioRpcError:  # type: ignore
            logger.exception(
                "Error occured in VehicleDataBrokerClient.GetMetadata",
            )
            raise
