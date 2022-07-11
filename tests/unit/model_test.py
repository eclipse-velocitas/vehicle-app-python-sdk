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

# pylint: disable=C0103,R0902,R0912,E1101

import asyncio
import threading
from unittest import mock

import grpc
import pytest

from sdv.base import Config
from sdv.model import (
    DataPointBoolean,
    DataPointBooleanArray,
    DataPointDouble,
    DataPointDoubleArray,
    DataPointFloat,
    DataPointFloatArray,
    DataPointInt8,
    DataPointInt8Array,
    DataPointInt16,
    DataPointInt16Array,
    DataPointInt32,
    DataPointInt32Array,
    DataPointInt64,
    DataPointInt64Array,
    DataPointString,
    DataPointStringArray,
    DataPointUint8,
    DataPointUint8Array,
    DataPointUint16,
    DataPointUint16Array,
    DataPointUint32,
    DataPointUint32Array,
    DataPointUint64,
    DataPointUint64Array,
    Dictionary,
    Model,
    ModelCollection,
    NamedRange,
)
from sdv.proto.broker_pb2 import GetDatapointsReply, SubscribeReply
from sdv.proto.types_pb2 import Datapoint
from sdv.vdb.client import VehicleDataBrokerClient


@pytest.fixture(autouse=True)
def setup_vdb_client():
    VehicleDataBrokerClient._instance = None


@pytest.mark.asyncio
async def test_thread_safe_query():
    vehicle = get_vehicle_instance()
    threads = []
    errors = []

    for i in range(20):
        thread = threading.Thread(
            target=entrypoint,
            args=(i, vehicle, errors),
        )
        threads.append(thread)
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    assert len(errors) == 0


async def run_query(i, k, vehicle, errors):
    if k % 3 == 0:
        query = await vehicle.Speed.where("X > 10").get_query()

        if query != "SELECT Vehicle.Speed WHERE X > 10":
            errors.append(
                f"""Thread: {i}, Task: {k}, Actual: {query},
                Expected: SELECT Vehicle.Speed WHERE X > 10"""
            )
    if k % 3 == 1:
        query = await vehicle.Speed.get_query()

        if query != "SELECT Vehicle.Speed":
            errors.append(
                f"Thread: {i}, Task: {k}, Actual: {query}, Expected: SELECT Vehicle.Speed"
            )
    if k % 3 == 2:
        query = await vehicle.Speed.join(
            vehicle.Cabin.Seat.element_at(1, 1).Position
        ).get_query()

        if query != "SELECT Vehicle.Speed, Vehicle.Cabin.Seat.Row1.Pos1.Position":
            errors.append(
                f"""Thread: {i}, Task: {k}, Actual: {query},
                Expected: SELECT Vehicle.Speed, Vehicle.Cabin.Seat.Row1.Pos1.Position"""
            )


def entrypoint(i, vehicle, errors):
    asyncio.set_event_loop(asyncio.new_event_loop())
    asyncio.run(asyncentrypoint(i, vehicle, errors))


async def asyncentrypoint(i, vehicle, errors):
    tasks = []
    for k in range(400):
        tasks.append(run_query(i, k, vehicle, errors))
    await asyncio.gather(*tasks, return_exceptions=True)


@pytest.mark.asyncio
async def test_get_exception():
    vehicle = get_vehicle_instance()
    with mock.patch.object(
        vehicle.Speed,
        "get_client",
        return_value=VehicleDataBrokerClient(12345),
    ):
        try:
            await vehicle.Speed.get()
        except Exception as ex:
            assert isinstance(ex, (grpc.aio.AioRpcError))


@pytest.mark.asyncio
async def test_string_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.String.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.String.get()
        assert (
            response == get_sample_datapoint("Vehicle.String", "Example").string_value
        )


@pytest.mark.asyncio
async def test_string_array_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.StringArray.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.StringArray.get()
        assert (
            response
            == get_sample_datapoint(
                "Vehicle.StringArray", ["Yes", "No"]
            ).string_array.values
        )


@pytest.mark.asyncio
async def test_bool_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Bool.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.Bool.get()
        assert response == get_sample_datapoint("Vehicle.Bool", True).bool_value


@pytest.mark.asyncio
async def test_bool_array_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.BoolArray.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.BoolArray.get()
        assert (
            response
            == get_sample_datapoint(
                "Vehicle.BoolArray", [True, False]
            ).bool_array.values
        )


@pytest.mark.asyncio
async def test_int8_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int8.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.Int8.get()
        assert response == get_sample_datapoint("Vehicle.Int8", 12).int32_value


@pytest.mark.asyncio
async def test_int8_array_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int8Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.Int8Array.get()
        assert (
            response
            == get_sample_datapoint(
                "Vehicle.Int8Array", [12, 13, 14]
            ).int32_array.values
        )


@pytest.mark.asyncio
async def test_int16_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int16.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.Int16.get()
        assert response == get_sample_datapoint("Vehicle.Int16", 144).int32_value


@pytest.mark.asyncio
async def test_int16_array_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int16Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.Int16Array.get()
        assert (
            response
            == get_sample_datapoint(
                "Vehicle.Int16Array", [98, 10, 34]
            ).int32_array.values
        )


@pytest.mark.asyncio
async def test_int32_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int32.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.Int32.get()
        assert response == get_sample_datapoint("Vehicle.Int32", 176).int32_value


@pytest.mark.asyncio
async def test_int32_array_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int32Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.Int32Array.get()
        assert (
            response
            == get_sample_datapoint(
                "Vehicle.Int32Array", [40, 50, 60]
            ).int32_array.values
        )


@pytest.mark.asyncio
async def test_int64_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int64.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.Int64.get()
        assert response == get_sample_datapoint("Vehicle.Int64", 999).int64_value


@pytest.mark.asyncio
async def test_int64_array_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int64Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.Int64Array.get()
        assert (
            response
            == get_sample_datapoint(
                "Vehicle.Int64Array", [70, 90, 1440]
            ).int64_array.values
        )


@pytest.mark.asyncio
async def test_uint8_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt8.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.UInt8.get()
        assert response == get_sample_datapoint("Vehicle.UInt8", 90).uint32_value


@pytest.mark.asyncio
async def test_uint16_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt16.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.UInt16.get()
        assert response == get_sample_datapoint("Vehicle.UInt16", 144).uint32_value


@pytest.mark.asyncio
async def test_uint16_array_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt16Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.UInt16Array.get()
        assert (
            response
            == get_sample_datapoint(
                "Vehicle.UInt16Array", [30, 40, 50]
            ).uint32_array.values
        )


@pytest.mark.asyncio
async def test_uint32_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt32.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.UInt32.get()
        assert response == get_sample_datapoint("Vehicle.UInt32", 234).uint32_value


@pytest.mark.asyncio
async def test_uint32_array_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt32Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.UInt32Array.get()
        assert (
            response
            == get_sample_datapoint(
                "Vehicle.UInt32Array", [81, 91, 101]
            ).uint32_array.values
        )


@pytest.mark.asyncio
async def test_uint64_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt64.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.UInt64.get()
        assert response == get_sample_datapoint("Vehicle.UInt64", 324).uint64_value


@pytest.mark.asyncio
async def test_uint64_array_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt64Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.UInt64Array.get()
        assert (
            response
            == get_sample_datapoint(
                "Vehicle.UInt64Array", [981, 971, 961]
            ).uint64_array.values
        )


@pytest.mark.asyncio
async def test_float_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Float.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.Float.get()
        assert response == get_sample_datapoint("Vehicle.Float", 321.0987).float_value


@pytest.mark.asyncio
async def test_float_array_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.FloatArray.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.FloatArray.get()
        assert (
            response
            == get_sample_datapoint(
                "Vehicle.FloatArray", [32.888, 67.9810, 124.67895]
            ).float_array.values
        )


@pytest.mark.asyncio
async def test_double_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Double.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.Double.get()
        assert (
            response == get_sample_datapoint("Vehicle.Double", 45678.98765).double_value
        )


@pytest.mark.asyncio
async def test_double_array_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.DoubleArray.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.DoubleArray.get()
        assert (
            response
            == get_sample_datapoint(
                "Vehicle.DoubleArray", [32.456789, 90.1234567, 100.01]
            ).double_array.values
        )


@pytest.mark.asyncio
async def test_uint8_array_value():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt8Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields("all")),
    ):
        response = await vehicle.UInt8Array.get()
        assert (
            response
            == get_sample_datapoint(
                "Vehicle.UInt8Array", [10, 20, 30]
            ).uint32_array.values
        )


@pytest.mark.asyncio
async def test_unsubscribe():
    vehicle = get_vehicle_instance()
    with mock.patch.object(
        vehicle.Speed.get_client(),
        "Subscribe",
        return_value=AsyncIter([SubscribeReply(fields=get_fields())]),
    ):
        rule = await vehicle.Speed.subscribe(callback)
        task = await rule.unsubscribe()
        assert task.cancelled()


@pytest.mark.asyncio
async def test_subscribe():
    vehicle = get_vehicle_instance()
    with mock.patch.object(
        vehicle.Speed.get_client(),
        "Subscribe",
        return_value=AsyncIter([SubscribeReply(fields=get_fields())]),
    ):
        try:
            await vehicle.Speed.subscribe(callback)
            # await vehicle.start()
        except Exception as ex:
            assert ex.args[0].fields["Vehicle.Speed"] == get_sample_datapoint("Speed")


@pytest.mark.asyncio
async def test_subscribe_with_join():
    vehicle = get_vehicle_instance()
    with mock.patch.object(
        vehicle.Speed.get_client(),
        "Subscribe",
        return_value=AsyncIter([SubscribeReply(fields=get_fields("JOIN"))]),
    ):
        try:
            (
                await vehicle.Speed.join(
                    vehicle.Cabin.Seat.element_at(1, 1).Position
                ).subscribe(callback_join)
            )
            # await vehicle.start()
        except Exception as ex:
            assert ex.args[0].fields["Vehicle.Speed"] == get_sample_datapoint("Speed")
            assert ex.args[0].fields[
                "Vehicle.Cabin.Seat.Row1.Pos1.Position"
            ] == get_sample_datapoint("Position")


@pytest.mark.asyncio
async def test_subscribe_with_where():
    vehicle = get_vehicle_instance()
    with mock.patch.object(
        vehicle.Speed.get_client(),
        "Subscribe",
        return_value=AsyncIter([SubscribeReply(fields=get_fields("WHERE > 0"))]),
    ):
        try:
            (
                await vehicle.Speed.where(
                    "Vehicle.Cabin.Seat.Row1.Pos1.Position > 0"
                ).subscribe(callback)
            )
            # await vehicle.start()
        except Exception as ex:
            assert ex.args[0].fields["Vehicle.Speed"] == get_sample_datapoint("Speed")


@pytest.mark.asyncio
async def test_subscribe_with_join_where():
    vehicle = get_vehicle_instance()
    with mock.patch.object(
        vehicle.Speed.get_client(),
        "Subscribe",
        return_value=AsyncIter([SubscribeReply(fields=get_fields("JOIN > 0"))]),
    ):
        try:
            (
                await vehicle.Speed.join(vehicle.Cabin.Seat.element_at(1, 1).Position)
                .where("Vehicle.Cabin.Seat.Row1.Pos1.Position > 0")
                .subscribe(callback_join)
            )
            # await vehicle.start()
        except Exception as ex:
            assert ex.args[0].fields["Vehicle.Speed"] == get_sample_datapoint("Speed")
            assert ex.args[0].fields[
                "Vehicle.Cabin.Seat.Row1.Pos1.Position"
            ] == get_sample_datapoint("Position")


async def test_get():
    vehicle = get_vehicle_instance()
    with mock.patch.object(
        vehicle.Speed.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=GetDatapointsReply(datapoints=get_fields()),
    ):
        response = await vehicle.Speed.get()
        assert response == get_sample_datapoint("Speed").float_value


@pytest.mark.asyncio
async def test_join():
    vehicle = get_vehicle_instance()
    query = (
        vehicle.Cabin.Seat.element_at(1, 2)
        .Position.join(vehicle.Speed, vehicle.Cabin.DriverPosition)
        .join(vehicle.Speed)
        .get_query()
    )
    expected_path = (
        "SELECT Vehicle.Cabin.Seat.Row1.Pos2.Position, Vehicle.Speed, "
        "Vehicle.Cabin.DriverPosition, Vehicle.Speed"
    )
    assert query == expected_path


@pytest.mark.asyncio
async def test_where():
    vehicle = get_vehicle_instance()
    query = (
        vehicle.Cabin.Seat.element_at(1, 2)
        .Position.where("Vehicle.Speed > 0")
        .get_query()
    )
    assert (
        query == "SELECT Vehicle.Cabin.Seat.Row1.Pos2.Position WHERE Vehicle.Speed > 0"
    )


@pytest.mark.asyncio
async def test_join_with_where():
    vehicle = get_vehicle_instance()
    query = (
        vehicle.Cabin.Seat.element_at(1, 2)
        .Position.join(vehicle.Speed, vehicle.Cabin.DriverPosition)
        .where("Vehicle.Speed > 0")
        .get_query()
    )
    assert query == (
        "SELECT Vehicle.Cabin.Seat.Row1.Pos2.Position, Vehicle.Speed,"
        " Vehicle.Cabin.DriverPosition WHERE Vehicle.Speed > 0"
    )


@pytest.mark.asyncio
async def test_multiple_join_with_where():
    vehicle = get_vehicle_instance()
    query = (
        vehicle.Cabin.Seat.element_at(1, 2)
        .Position.join(vehicle.Speed, vehicle.Cabin.DriverPosition)
        .join(vehicle.Cabin)
        .where("Vehicle.Speed > 0")
        .get_query()
    )
    assert query == (
        "SELECT Vehicle.Cabin.Seat.Row1.Pos2.Position, Vehicle.Speed, "
        "Vehicle.Cabin.DriverPosition, Vehicle.Cabin WHERE Vehicle.Speed > 0"
    )


def test_path_depth2():
    vehicle = get_vehicle_instance()
    path = vehicle.Speed.get_path()
    assert path == "Vehicle.Speed"


def test_path_depth3():
    vehicle = get_vehicle_instance()
    path = vehicle.Cabin.DriverPosition.get_path()
    assert path == "Vehicle.Cabin.DriverPosition"


def test_path_instances_range2():
    vehicle = get_vehicle_instance()
    path = vehicle.Cabin.Seat.element_at(1, 2).Position.get_path()
    assert path == "Vehicle.Cabin.Seat.Row1.Pos2.Position"


def test_path_instances_range_list():
    vehicle = get_vehicle_instance()
    path = vehicle.Cabin.Door.element_at(1, DoorSides[0]).IsOpen.get_path()
    assert path == "Vehicle.Cabin.Door.Row1.Left.IsOpen"


def test_path_instances_dictionary():
    vehicle = get_vehicle_instance()
    path = vehicle.Body.Trunk.element_at("Rear").IsOpen.get_path()
    assert path == "Vehicle.Body.Trunk.Rear.IsOpen"


def test_path_unknown_list_entry():
    vehicle = get_vehicle_instance()
    try:
        vehicle.Cabin.Door.element_at(1, "Middle").IsOpen.get_path()
        raise AssertionError()
    except ValueError as e:
        assert e.args[0] == "Middle is not in ['Left', 'Right']"


def test_path_out_of_range():
    vehicle = get_vehicle_instance()
    try:
        vehicle.Cabin.Seat.element_at(5, 5).Position.get_path()
        raise AssertionError()
    except ValueError as e:
        assert e.args[0] == "5 is not in range 1-2"


DoorSides = ["Left", "Right"]
TrunkOptions = ["Front", "Rear"]


class AsyncIter:
    """AsyncIter"""

    def __init__(self, items):
        self.items = items

    async def __aiter__(self):
        for item in self.items:
            yield item


async def callback(response):
    raise Exception(response)


async def callback_join(response):
    raise Exception(response)


def raise_exception(expection):
    raise expection


def get_fields(condition=""):
    data = {}
    if condition == "":
        data["Vehicle.Speed"] = get_sample_datapoint("Speed")
    elif condition == "JOIN":
        data["Vehicle.Speed"] = get_sample_datapoint("Speed")
        data["Vehicle.Cabin.Seat.Row1.Pos1.Position"] = get_sample_datapoint("Position")
    elif condition == "all":
        sample_data = {
            "Vehicle.String": "Example",
            "Vehicle.Bool": True,
            "Vehicle.Int8": 12,
            "Vehicle.Int16": 144,
            "Vehicle.Int32": 176,
            "Vehicle.Int64": 999,
            "Vehicle.UInt8": 90,
            "Vehicle.UInt16": 144,
            "Vehicle.UInt32": 234,
            "Vehicle.UInt64": 324,
            "Vehicle.Float": 321.0987,
            "Vehicle.Double": 45678.98765,
            "Vehicle.StringArray": ["Yes", "No"],
            "Vehicle.BoolArray": [True, False],
            "Vehicle.Int8Array": [12, 13, 14],
            "Vehicle.Int16Array": [98, 10, 34],
            "Vehicle.Int32Array": [40, 50, 60],
            "Vehicle.Int64Array": [70, 90, 1440],
            "Vehicle.UInt8Array": [10, 20, 30],
            "Vehicle.UInt16Array": [30, 40, 50],
            "Vehicle.UInt32Array": [81, 91, 101],
            "Vehicle.UInt64Array": [981, 971, 961],
            "Vehicle.FloatArray": [32.888, 67.9810, 124.67895],
            "Vehicle.DoubleArray": [32.456789, 90.1234567, 100.01],
        }
        for name in sample_data.items():
            data[name[0]] = get_sample_datapoint(name[0], name[1])
    else:
        conditions = condition.split(" ")
        data["Vehicle.Speed"] = get_sample_datapoint("Speed")
        data["Vehicle.Cabin.Seat.Row1.Pos1.Position"] = get_sample_datapoint("Position")

        if conditions[1] == ">" and data[
            "Vehicle.Cabin.Seat.Row1.Pos1.Position"
        ].int32_value < int(conditions[2]):
            return {}

        if conditions[0] == "WHERE":
            data.pop("Vehicle.Cabin.Seat.Row1.Pos1.Position")

    return data


def get_sample_datapoint(data, value=10) -> Datapoint:
    datapoint = Datapoint()
    if data == "Speed":
        datapoint.float_value = float(value)
    if data == "Position":
        datapoint.int32_value = int(value)
    if data == "Vehicle.String":
        datapoint.string_value = str(value)
    if data == "Vehicle.Bool":
        datapoint.bool_value = value
    if data == "Vehicle.Float":
        datapoint.float_value = value
    if data in ["Vehicle.Int8", "Vehicle.Int16", "Vehicle.Int32"]:
        datapoint.int32_value = value
    if data == "Vehicle.Int64":
        datapoint.int64_value = value
    if data in ["Vehicle.UInt8", "Vehicle.UInt16", "Vehicle.UInt32"]:
        datapoint.uint32_value = value
    if data == "Vehicle.UInt64":
        datapoint.uint64_value = value
    if data == "Vehicle.Double":
        datapoint.double_value = value
    if data == "Vehicle.StringArray":
        datapoint.string_array.values.extend(value)
    if data == "Vehicle.BoolArray":
        datapoint.bool_array.values.extend(value)
    if data in ["Vehicle.Int8Array", "Vehicle.Int16Array", "Vehicle.Int32Array"]:
        datapoint.int32_array.values.extend(value)
    if data == "Vehicle.Int64Array":
        datapoint.int64_array.values.extend(value)
    if data in ["Vehicle.UInt8Array", "Vehicle.UInt16Array", "Vehicle.UInt32Array"]:
        datapoint.uint32_array.values.extend(value)
    if data == "Vehicle.UInt64Array":
        datapoint.uint64_array.values.extend(value)
    if data == "Vehicle.DoubleArray":
        datapoint.double_array.values.extend(value)
    return datapoint


def get_vehicle_instance():
    class Seat(Model):
        """Seat Class"""

        def __init__(self, parent):
            super().__init__(parent)
            self.Position = DataPointBoolean("Position", self)

    class Door(Model):
        """Door Class"""

        def __init__(self, parent):
            super().__init__(parent)
            self.IsOpen = DataPointBoolean("IsOpen", self)

    class Cabin(Model):
        """Cabin Class"""

        def __init__(self, parent):
            super().__init__(parent)
            self.DriverPosition = DataPointBoolean("DriverPosition", self)
            self.Seat = ModelCollection[Seat](
                [NamedRange("Row", 1, 2), NamedRange("Pos", 1, 3)], Seat(self)
            )
            self.Door = ModelCollection[Door](
                [NamedRange("Row", 1, 2), Dictionary(DoorSides)],
                Door(self),
            )
    
    class Trunk(Model):
        """Trunk Class"""

        def __init__(self, parent):
            super().__init__(parent)
            self.IsOpen = DataPointBoolean("IsOpen", self)
            self.IsLocked = DataPointBoolean("IsLocked", self)

    class Body(Model):
        """Body Class"""

        def __init__(self, parent):
            super().__init__(parent)
            self.Trunk = ModelCollection[Trunk]([Dictionary(TrunkOptions)], Trunk(self))

    class Vehicle(Model):
        """Mock Class"""

        def __init__(self):
            super().__init__()
            self.Speed = DataPointFloat("Speed", self)
            self.Cabin = Cabin(self)
            self.Body = Body(self)
            self.String = DataPointString("String", self)
            self.Bool = DataPointBoolean("Bool", self)
            self.Int8 = DataPointInt8("Int8", self)
            self.Int16 = DataPointInt16("Int16", self)
            self.Int32 = DataPointInt32("Int32", self)
            self.Int64 = DataPointInt64("Int64", self)
            self.UInt8 = DataPointUint8("UInt8", self)
            self.UInt16 = DataPointUint16("UInt16", self)
            self.UInt32 = DataPointUint32("UInt32", self)
            self.UInt64 = DataPointUint64("UInt64", self)
            self.Float = DataPointFloat("Float", self)
            self.Double = DataPointDouble("Double", self)
            self.StringArray = DataPointStringArray("StringArray", self)
            self.BoolArray = DataPointBooleanArray("BoolArray", self)
            self.Int8Array = DataPointInt8Array("Int8Array", self)
            self.Int16Array = DataPointInt16Array("Int16Array", self)
            self.Int32Array = DataPointInt32Array("Int32Array", self)
            self.Int64Array = DataPointInt64Array("Int64Array", self)
            self.UInt8Array = DataPointUint8Array("UInt8Array", self)
            self.UInt16Array = DataPointUint16Array("UInt16Array", self)
            self.UInt32Array = DataPointUint32Array("UInt32Array", self)
            self.UInt64Array = DataPointUint64Array("UInt64Array", self)
            self.FloatArray = DataPointFloatArray("FloatArray", self)
            self.DoubleArray = DataPointDoubleArray("DoubleArray", self)

    Config().disable_dapr()
    vehicle = Vehicle()
    # vehicle.get_client()
    return vehicle
