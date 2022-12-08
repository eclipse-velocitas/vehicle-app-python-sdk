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
import os
from typing import List, Optional

import grpc

from sdv.proto.broker_pb2 import (
    GetDatapointsRequest,
    GetMetadataRequest,
    SetDatapointsRequest,
    SubscribeRequest,
)
from sdv.proto.broker_pb2_grpc import BrokerStub

from .. import conf

logger = logging.getLogger(__name__)


class VehicleDataBrokerClient:
    """VehicleDataBrokerClient provides the Graph API to access vehicle services
    and vehicle signals."""

    _instance = None

    def __new__(cls, port: Optional[int] = None):
        if cls._instance is None:
            cls._instance = super(VehicleDataBrokerClient, cls).__new__(cls)
            if not conf.DISABLE_DAPR:
                if port is None:
                    port = int(str(os.getenv("DAPR_GRPC_PORT")))
                cls._address = f"localhost:{port}"
            else:
                cls._address = conf.VEHICLE_DATA_BROKER_ADDRESS

            cls._channel = grpc.aio.insecure_channel(cls._address)  # type: ignore
            appid = conf.VEHICLE_DATA_BROKER_APP_ID
            cls._metadata = (("dapr-app-id", appid),)
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
