# Copyright (c) 2022-2023 Contributors to the Eclipse Foundation
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

""" Tests for methods in VehicleDataBrokerClient """

import os

os.environ["SDV_MIDDLEWARE_TYPE"] = "native"
from unittest import mock

import grpc
import pytest

from velocitas_sdk import config
from velocitas_sdk.test.databroker_testhelper import SubscribeException, Vehicle
from velocitas_sdk.test.inttesthelper import IntTestHelper
from velocitas_sdk.vdb.client import VehicleDataBrokerClient
from velocitas_sdk.vehicle_app import VehicleApp


@pytest.fixture(autouse=True)
def reset():
    VehicleDataBrokerClient._instance = None
    config._config = None


@pytest.mark.asyncio
async def test_for_get_metadata():
    client = get_vehicleapp_instance()
    response = await client._vdb_client.GetMetadata([])
    assert response is not None


@pytest.mark.asyncio
async def test_for_get_datapoint():
    client = get_vehicleapp_instance()
    datapoint = []
    metadatas = await client._vdb_client.GetMetadata([])
    for metadata in metadatas.list:
        datapoint.append(metadata.name)
    response = await client._vdb_client.GetDatapoints(datapoint)
    assert response is not None
    assert len(response.datapoints) == len(datapoint)


@pytest.mark.asyncio
async def test_for_subscribe():
    client = get_vehicleapp_instance()
    datapoint = "Vehicle.Speed"
    await change_datapoint(datapoint, 0.0)
    query = "SELECT " + datapoint
    updated = 0
    async for reply in client._vdb_client.Subscribe(query):
        updated += 1
        await callback(reply, datapoint)
        if updated == 2:
            break

    assert reply.fields[datapoint].float_value == 100.0


@pytest.mark.asyncio
async def test_for_subscribe_where_clause():
    client = get_vehicleapp_instance()
    datapoint = "Vehicle.Speed"
    await change_datapoint(datapoint, 150.0)
    query = "SELECT " + datapoint + " WHERE Vehicle.Speed > 100.0"
    updated = 0
    async for reply in client._vdb_client.Subscribe(query):
        updated += 1
        await callback(reply, datapoint)
        if updated == 2:
            break

    assert reply.fields[datapoint].float_value == 250.0


@pytest.mark.asyncio
async def test_for_subscribe_join():
    client = get_vehicleapp_instance()
    datapoint = "Vehicle.Speed"
    await change_datapoint(datapoint, 50.0)
    await change_datapoint("Vehicle.ThisIsAFloat", 0.0)
    query = "SELECT Vehicle.ThisIsAFloat, " + datapoint
    updated = 0
    async for reply in client._vdb_client.Subscribe(query):
        updated += 1
        await callback(reply, datapoint)
        if updated == 1:
            break

    assert reply.fields[datapoint].float_value == 100.0
    assert reply.fields["Vehicle.ThisIsAFloat"].float_value == 50.0


@pytest.mark.asyncio
async def test_for_subscribe_join_where():
    client = get_vehicleapp_instance()
    datapoint = "Vehicle.Speed"
    await change_datapoint(datapoint, 50.0)
    await change_datapoint("Vehicle.ThisIsAFloat", 0.0)
    query = (
        "SELECT Vehicle.ThisIsAFloat, "
        + datapoint
        + " WHERE Vehicle.ThisIsAFloat > 10.0"
    )
    updated = 0
    async for reply in client._vdb_client.Subscribe(query):
        updated += 1
        await callback(reply, datapoint)
        if updated == 1:
            break

    assert reply.fields[datapoint].float_value == 100.0
    assert reply.fields["Vehicle.ThisIsAFloat"].float_value == 50.0


@pytest.mark.asyncio
async def test_for_fluent_get():
    # with mock.patch.dict(os.environ, {"DAPR_GRPC_PORT": "55555"}):
    vehicle = get_vehicle_instance()
    await change_datapoint(vehicle.Speed.get_path(), 0.0)
    response = await vehicle.Speed.get()
    assert response.value == 50.0


@pytest.mark.asyncio
async def test_for_fluent_unsubscribe():
    with mock.patch.dict(os.environ, {"DAPR_GRPC_PORT": "55555"}):
        vehicle = get_vehicle_instance()
    await change_datapoint(vehicle.Speed.get_path(), 0.0)
    rule = await vehicle.Speed.subscribe(callback_fluent)
    task = await rule.unsubscribe()
    assert task.cancelled()


@pytest.mark.asyncio
async def test_for_fluent_resubscribe():
    with mock.patch.dict(os.environ, {"DAPR_GRPC_PORT": "55555"}):
        vehicle = get_vehicle_instance()
    await change_datapoint(vehicle.Speed.get_path(), 0.0)
    task = None
    try:
        rule = await vehicle.Speed.subscribe(callback_fluent)
        task = await rule.unsubscribe()
        rule = await rule.subscribe()
        # await vehicle.start()
    except SubscribeException as e:
        assert task.cancelled()
        assert e.datapoint.fields["Vehicle.Speed"].float_value == 50.0


@pytest.mark.asyncio
async def test_for_fluent_subscribe():
    with mock.patch.dict(os.environ, {"DAPR_GRPC_PORT": "55555"}):
        vehicle = get_vehicle_instance()
    await change_datapoint(vehicle.Speed.get_path(), 0.0)
    try:
        await vehicle.Speed.subscribe(callback_fluent)
        # await vehicle.start()
    except SubscribeException as e:
        assert e.datapoint.fields["Vehicle.Speed"].float_value == 50.0


def callback_fluent(data):
    raise SubscribeException(data)


@pytest.mark.asyncio
async def test_for_fluent_join():
    with mock.patch.dict(os.environ, {"DAPR_GRPC_PORT": "55555"}):
        vehicle = get_vehicle_instance()
    await change_datapoint(vehicle.Speed.get_path(), 0.0)
    await change_datapoint(vehicle.ThisIsAFloat.get_path(), 50.0)
    try:
        await vehicle.Speed.join(vehicle.ThisIsAFloat).subscribe(callback_fluent)
        # await vehicle.start()
    except SubscribeException as e:
        assert e.datapoint.fields["Vehicle.Speed"].float_value == 50.0
        assert e.datapoint.fields["Vehicle.ThisIsAFloat"].float_value == 100.0


@pytest.mark.asyncio
async def test_for_fluent_where():
    with mock.patch.dict(os.environ, {"DAPR_GRPC_PORT": "55555"}):
        vehicle = get_vehicle_instance()
    await change_datapoint(vehicle.Speed.get_path(), 0.0)
    try:
        await vehicle.Speed.where("Vehicle.Speed < 60.0").subscribe(callback_fluent)
        # await vehicle.start()
    except SubscribeException as e:
        assert e.datapoint.fields["Vehicle.Speed"].float_value == 50.0


@pytest.mark.asyncio
async def test_for_fluent_where_join():
    # with mock.patch.dict(os.environ, {"DAPR_GRPC_PORT": "55555"}):
    vehicle = get_vehicle_instance()
    await change_datapoint(vehicle.Speed.get_path(), 0.0)
    await change_datapoint(vehicle.ThisIsAFloat.get_path(), 50.0)
    try:
        await vehicle.Speed.join(vehicle.ThisIsAFloat).where(
            "Vehicle.Speed < 60.0"
        ).subscribe(callback_fluent)
        # await vehicle.start()
    except SubscribeException as e:
        assert e.datapoint.fields["Vehicle.Speed"].float_value == 50.0
        assert e.datapoint.fields["Vehicle.ThisIsAFloat"].float_value == 100.0


@pytest.mark.asyncio
async def test_for_subscribe_exception():
    with mock.patch.dict(os.environ, {"DAPR_GRPC_PORT": "55555"}):
        vehicle = get_vehicle_instance()
    await change_datapoint(vehicle.Speed.get_path(), 0.0)
    try:
        await vehicle.Speed.where("GIVE ERROR").subscribe(callback_fluent)
        # await vehicle.start()
    except Exception as e:
        assert isinstance(e, (grpc.aio.AioRpcError))


async def callback(reply, datapoint):
    speed = reply.fields[datapoint].float_value
    await change_datapoint(datapoint, speed)


def get_vehicleapp_instance():
    client = VehicleApp()
    return client


async def change_datapoint(datapoint, value):
    client = IntTestHelper()
    value += 50.0
    await client.set_float_datapoint(datapoint, value)


def get_vehicle_instance():
    vehicle = Vehicle()
    return vehicle
