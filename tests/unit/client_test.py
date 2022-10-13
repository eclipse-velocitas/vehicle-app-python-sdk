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

""" Tests for methods in VehicleClient """

import os
import sys
from typing import Mapping, Text
from unittest import mock

import pytest

from sdv.proto.broker_pb2 import (
    GetDatapointsReply,
    GetMetadataReply,
    SetDatapointsReply,
    SubscribeReply,
)
from sdv.proto.types_pb2 import Datapoint, DataType, Metadata
from sdv.vdb.client import VehicleDataBrokerClient

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))


@pytest.mark.asyncio
async def test_for_get_metadata():

    client = get_vehicle_client_instance()

    with mock.patch.object(
        client._stub,
        "GetMetadata",
        new_callable=mock.AsyncMock,
        return_value=GetMetadataReply(list=[get_sample_metadata()]),
    ):
        response = await client.GetMetadata(["Vehicle.Speed"])
        assert response.list[0] == get_sample_metadata()
        await client.close()


@pytest.mark.asyncio
async def test_for_get_data_points():
    client = get_vehicle_client_instance()

    with mock.patch.object(
        client._stub,
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields()),
    ):
        response = await client.GetDatapoints(["Vehicle.Speed"])
        assert (
            response.datapoints["Vehicle.Speed"].int32_value
            == get_sample_datapoint().int32_value
        )
        await client.close()


@pytest.mark.asyncio
async def test_for_set_datapoints():
    client = get_vehicle_client_instance()

    with mock.patch.object(
        client._stub,
        "SetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=SetDatapointsReply(errors=datapoint_set_success()),
    ):
        datapoint = get_sample_datapoint()
        response = await client.SetDatapoints(datapoints={"Vehicle.Speed": datapoint})
        # The response has an empty error
        assert response.errors == {}
        await client.close()


@pytest.mark.asyncio
async def test_for_set_datapoints_error():
    client = get_vehicle_client_instance()

    with mock.patch.object(
        client._stub,
        "SetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=SetDatapointsReply(errors=datapoint_set_error()),
    ):
        datapoint = get_sample_datapoint()
        response = await client.SetDatapoints(datapoints={"Vehicle.Speed": datapoint})
        # The response.errors is not empty. I.e. has an error = datapoint_set_error()
        assert bool(response.errors)
        await client.close()


@pytest.mark.asyncio
async def test_for_subscribe():
    client = get_vehicle_client_instance()

    with mock.patch.object(
        client._stub,
        "Subscribe",
        return_value=SubscribeReply(fields=get_fields()),
    ):
        response = client.Subscribe("SELECT Vehicle.Speed")
        assert (
            response.fields["Vehicle.Speed"].int32_value
            == get_sample_datapoint().int32_value
        )
        await client.close()


# Mock data


def get_fields() -> Mapping[Text, Datapoint]:
    data = {}
    data["Vehicle.Speed"] = get_sample_datapoint()
    return data


def datapoint_set_success() -> Mapping[Text, int]:
    return {}


def get_sample_datapoint() -> Datapoint:
    datapoint = Datapoint()
    datapoint.int32_value = 0

    return datapoint


def datapoint_set_error() -> Mapping[Text, Datapoint]:
    error = {}
    error["Vehicle.Speed"] = 0
    return error


def get_vehicle_client_instance():
    client = VehicleDataBrokerClient(50051)
    return client


def get_sample_metadata() -> Metadata:
    metadata = Metadata()
    metadata.id = 1
    metadata.data_type = DataType.FLOAT
    metadata.name = "Vehicle.Speed"
    return metadata
