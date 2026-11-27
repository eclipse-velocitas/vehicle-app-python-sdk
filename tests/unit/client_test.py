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


"""Tests for methods in VehicleClient"""

import os
import sys
from collections.abc import Mapping
from unittest import mock

import grpc
import pytest

from velocitas_sdk import config
from velocitas_sdk.config import Config
from velocitas_sdk.proto.types_pb2 import Datapoint, DataType, Metadata
from velocitas_sdk.proto.val_pb2 import (
    BatchActuateResponse,
    GetValuesResponse,
    ListMetadataResponse,
    SubscribeResponse,
)
from velocitas_sdk.vdb.client import VehicleDataBrokerClient

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))


@pytest.fixture(autouse=True)
def reset():
    config._config = Config("native")
    config.middleware = config._config.middleware


@pytest.mark.asyncio
async def test_for_get_metadata():
    client = get_vehicle_client_instance()

    with mock.patch.object(
        client._stub,
        "ListMetadata",
        new_callable=mock.AsyncMock,
        return_value=ListMetadataResponse(metadata=[get_sample_metadata()]),
    ):
        response = await client.GetMetadata(["Vehicle.Speed"])
        assert response[0] == get_sample_metadata()
        await client.close()


@pytest.mark.asyncio
async def test_for_get_data_points():
    client = get_vehicle_client_instance()

    with mock.patch.object(
        client._stub,
        "GetValues",
        new_callable=mock.AsyncMock,
        return_value=GetValuesResponse(data_points=[get_sample_datapoint()]),
    ):
        response = await client.GetDatapoints(["Vehicle.Speed"])
        assert (
            response["Vehicle.Speed"].value.int32 == get_sample_datapoint().value.int32
        )
        await client.close()


@pytest.mark.asyncio
async def test_for_set_datapoints():
    client = get_vehicle_client_instance()

    with mock.patch.object(
        client._stub,
        "BatchActuate",
        new_callable=mock.AsyncMock,
        return_value=BatchActuateResponse(),
    ):
        datapoint = get_sample_datapoint()
        await client.SetDatapoints(datapoints={"Vehicle.Speed": datapoint})
        # The response is empty
        await client.close()


@pytest.mark.asyncio
async def test_for_set_datapoints_error():
    client = get_vehicle_client_instance()

    with mock.patch.object(
        client._stub,
        "BatchActuate",
        new_callable=mock.AsyncMock,
        side_effect=grpc.aio.AioRpcError(grpc.StatusCode.NOT_FOUND, "", ""),
    ):
        datapoint = get_sample_datapoint()
        with pytest.raises(grpc.aio.AioRpcError):
            await client.SetDatapoints(datapoints={"Unknown.Signal": datapoint})
        await client.close()


@pytest.mark.asyncio
async def test_for_subscribe():
    client = get_vehicle_client_instance()

    with mock.patch.object(
        client._stub,
        "Subscribe",
        return_value=SubscribeResponse(entries=get_fields()),
    ):
        response = client.Subscribe("SELECT Vehicle.Speed, Vehicle.Acceleration")
        assert (
            response.entries["Vehicle.Speed"].value.int32
            == get_sample_datapoint().value.int32
        )
        assert (
            response.entries["Vehicle.Acceleration"].value.int32
            == get_sample_datapoint().value.int32
        )
        await client.close()


@pytest.mark.asyncio
async def test_for_subscribing_empty_list():
    client = get_vehicle_client_instance()

    with (
        mock.patch.object(client._stub, "Subscribe", sideeffect=ValueError),
        pytest.raises(ValueError),
    ):
        client.Subscribe("SELECT ")
        await client.close()


@pytest.mark.asyncio
async def test_for_subscribing_malformed_list():
    client = get_vehicle_client_instance()

    with (
        mock.patch.object(client._stub, "Subscribe", sideeffect=ValueError),
        pytest.raises(ValueError),
    ):
        client.Subscribe("SELECT Vehicle.Speed,,Whatever ")
        await client.close()


# Mock data


def get_fields() -> Mapping[str, Datapoint]:
    data = {}
    data["Vehicle.Speed"] = get_sample_datapoint()
    data["Vehicle.Acceleration"] = get_sample_datapoint()
    return data


def get_sample_datapoint() -> Datapoint:
    datapoint = Datapoint()
    datapoint.value.int32 = 0

    return datapoint


def get_vehicle_client_instance():
    client = VehicleDataBrokerClient(50051)
    return client


def get_sample_metadata() -> Metadata:
    metadata = Metadata()
    metadata.id = 1
    metadata.data_type = DataType.DATA_TYPE_FLOAT
    metadata.path = "Vehicle.Speed"
    return metadata
