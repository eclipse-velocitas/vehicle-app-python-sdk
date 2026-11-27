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
import threading
from unittest import TestCase, mock

import grpc
import pytest

from velocitas_sdk import config
from velocitas_sdk.model import (
    DataPoint,
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
    Model,
)
from velocitas_sdk.proto.types_pb2 import Datapoint as BrokerDatapoint
from velocitas_sdk.proto.val_pb2 import (
    SubscribeResponse,
)
from velocitas_sdk.vdb.client import VehicleDataBrokerClient
from velocitas_sdk.vdb.reply import DataPointReply


@pytest.fixture(autouse=True)
def reset():
    VehicleDataBrokerClient._instance = None
    config._config = None


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
    if k % 3 == 1:
        query = await vehicle.Speed.get_query()

        if query != "SELECT Vehicle.Speed":
            errors.append(
                f"Thread: {i}, Task: {k}, Actual: {query}, \
                    Expected: SELECT Vehicle.Speed"
            )
    if k % 3 == 2:
        query = await vehicle.Speed.join(
            vehicle.Cabin.Seat.Row1.DriverSide.Position
        ).get_query()

        if query != "SELECT Vehicle.Speed, Vehicle.Cabin.Seat.Row1.DriverSide.Position":
            errors.append(
                f"""Thread: {i}, Task: {k}, Actual: {query},
                Expected: SELECT Vehicle.Speed, Vehicle.Cabin.Seat.Row1.DriverSide.Position"""
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
    with (
        mock.patch.object(
            vehicle.Speed,
            "get_client",
            side_effect=grpc.aio.AioRpcError("Something went wrong", "", ""),
        ),
        pytest.raises(grpc.aio.AioRpcError),
    ):
        await vehicle.Speed.get()


def test_try_create_unspecific():
    unspecific = DataPoint("unspecific", None)

    with pytest.raises(TypeError):
        unspecific.create_broker_data_point(42)


def test_create_string():
    vehicle = get_vehicle_instance()

    test_value = "huhu"
    broker_data_point = vehicle.String.create_broker_data_point(test_value)
    assert broker_data_point.value.HasField("string")
    assert broker_data_point.value.string == test_value


@pytest.mark.asyncio
async def test_get_string():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.String.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.String.get()
        assert (
            response.value
            == get_sample_datapoint("Vehicle.String", "Example").value.string
        )


@pytest.mark.asyncio
async def test_set_string():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.String.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.String.set("New Value")
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_string_array():
    vehicle = get_vehicle_instance()

    expected_array = ["huhu", "Sarah"]
    broker_data_point = vehicle.StringArray.create_broker_data_point(expected_array)

    assert broker_data_point.value.HasField("string_array")
    actual_array = broker_data_point.value.string_array.values
    assert len(expected_array) == len(actual_array)
    for expected_value, actual_value in zip(expected_array, actual_array):
        assert expected_value == actual_value


@pytest.mark.asyncio
async def test_get_string_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.StringArray.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.StringArray.get()
        assert (
            response.value
            == get_sample_datapoint(
                "Vehicle.StringArray", ["Yes", "No"]
            ).value.string_array.values
        )


@pytest.mark.asyncio
async def test_set_string_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.StringArray.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.StringArray.set(["Yes", "No", "YO"])
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_bool():
    vehicle = get_vehicle_instance()

    test_value = True
    broker_data_point = vehicle.Bool.create_broker_data_point(test_value)
    assert broker_data_point.value.HasField("bool")
    assert broker_data_point.value.bool == test_value


@pytest.mark.asyncio
async def test_get_bool():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Bool.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.Bool.get()
        assert response.value == get_sample_datapoint("Vehicle.Bool", True).value.bool


@pytest.mark.asyncio
async def test_set_bool():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Bool.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.Bool.set(False)
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_bool_array():
    vehicle = get_vehicle_instance()

    expected_array = [True, False]
    broker_data_point = vehicle.BoolArray.create_broker_data_point(expected_array)

    assert broker_data_point.value.HasField("bool_array")
    actual_array = broker_data_point.value.bool_array.values
    assert len(expected_array) == len(actual_array)
    for expected_value, actual_value in zip(expected_array, actual_array):
        assert expected_value == actual_value


@pytest.mark.asyncio
async def test_get_bool_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.BoolArray.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.BoolArray.get()
        assert (
            response.value
            == get_sample_datapoint(
                "Vehicle.BoolArray", [True, False]
            ).value.bool_array.values
        )


@pytest.mark.asyncio
async def test_set_bool_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.BoolArray.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.BoolArray.set([False, True])
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_int8():
    vehicle = get_vehicle_instance()

    test_value = -128
    broker_data_point = vehicle.Int8.create_broker_data_point(test_value)
    assert broker_data_point.value.HasField("int32")
    assert broker_data_point.value.int32 == test_value


@pytest.mark.asyncio
async def test_get_int8():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int8.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.Int8.get()
        assert response.value == get_sample_datapoint("Vehicle.Int8", 12).value.int32


@pytest.mark.asyncio
async def test_set_int8():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int8.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.Int8.set(10)
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_int8_array():
    vehicle = get_vehicle_instance()

    expected_array = [-128, 127]
    broker_data_point = vehicle.Int8Array.create_broker_data_point(expected_array)

    assert broker_data_point.value.HasField("int32_array")
    actual_array = broker_data_point.value.int32_array.values
    assert len(expected_array) == len(actual_array)
    for expected_value, actual_value in zip(expected_array, actual_array):
        assert expected_value == actual_value


@pytest.mark.asyncio
async def test_get_int8_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int8Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.Int8Array.get()
        assert (
            response.value
            == get_sample_datapoint(
                "Vehicle.Int8Array", [12, 13, 14]
            ).value.int32_array.values
        )


@pytest.mark.asyncio
async def test_set_int8_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int8Array.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.Int8Array.set([15, 16, 17])
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_int16():
    vehicle = get_vehicle_instance()

    test_value = -32768
    broker_data_point = vehicle.Int16.create_broker_data_point(test_value)
    assert broker_data_point.value.HasField("int32")
    assert broker_data_point.value.int32 == test_value


@pytest.mark.asyncio
async def test_get_int16():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int16.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.Int16.get()
        assert response.value == get_sample_datapoint("Vehicle.Int16", 144).value.int32


@pytest.mark.asyncio
async def test_set_int16():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int16.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.Int16.set(10)
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_int16_array():
    vehicle = get_vehicle_instance()

    expected_array = [-32768, 32767]
    broker_data_point = vehicle.Int16Array.create_broker_data_point(expected_array)

    assert broker_data_point.value.HasField("int32_array")
    actual_array = broker_data_point.value.int32_array.values
    assert len(expected_array) == len(actual_array)
    for expected_value, actual_value in zip(expected_array, actual_array):
        assert expected_value == actual_value


@pytest.mark.asyncio
async def test_get_int16_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int16Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.Int16Array.get()
        assert (
            response.value
            == get_sample_datapoint(
                "Vehicle.Int16Array", [98, 10, 34]
            ).value.int32_array.values
        )


@pytest.mark.asyncio
async def test_set_int16_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int16Array.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.Int16Array.set([10, 20, 30])
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_int32():
    vehicle = get_vehicle_instance()

    test_value = -2147483648
    broker_data_point = vehicle.Int32.create_broker_data_point(test_value)
    assert broker_data_point.value.HasField("int32")
    assert broker_data_point.value.int32 == test_value


@pytest.mark.asyncio
async def test_get_int32():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int32.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.Int32.get()
        assert response.value == get_sample_datapoint("Vehicle.Int32", 176).value.int32


@pytest.mark.asyncio
async def test_set_int32():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int32.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.Int32.set(10)
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_int32_array():
    vehicle = get_vehicle_instance()

    expected_array = [-2147483648, 2147483647]
    broker_data_point = vehicle.Int32Array.create_broker_data_point(expected_array)

    assert broker_data_point.value.HasField("int32_array")
    actual_array = broker_data_point.value.int32_array.values
    assert len(expected_array) == len(actual_array)
    for expected_value, actual_value in zip(expected_array, actual_array):
        assert expected_value == actual_value


@pytest.mark.asyncio
async def test_get_int32_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int32Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.Int32Array.get()
        assert (
            response.value
            == get_sample_datapoint(
                "Vehicle.Int32Array", [40, 50, 60]
            ).value.int32_array.values
        )


@pytest.mark.asyncio
async def test_set_int32_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int32Array.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.Int32Array.set([60, 70, 80])
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_int64():
    vehicle = get_vehicle_instance()

    test_value = -9223372036854775808
    broker_data_point = vehicle.Int64.create_broker_data_point(test_value)
    assert broker_data_point.value.HasField("int64")
    assert broker_data_point.value.int64 == test_value


@pytest.mark.asyncio
async def test_get_int64():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int64.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.Int64.get()
        assert response.value == get_sample_datapoint("Vehicle.Int64", 999).value.int64


@pytest.mark.asyncio
async def test_set_int64():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int64.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.Int64.set(9999)
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_int64_array():
    vehicle = get_vehicle_instance()

    expected_array = [-9223372036854775808, 9223372036854775807]
    broker_data_point = vehicle.Int64Array.create_broker_data_point(expected_array)

    assert broker_data_point.value.HasField("int64_array")
    actual_array = broker_data_point.value.int64_array.values
    assert len(expected_array) == len(actual_array)
    for expected_value, actual_value in zip(expected_array, actual_array):
        assert expected_value == actual_value


@pytest.mark.asyncio
async def test_get_int64_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int64Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.Int64Array.get()
        assert (
            response.value
            == get_sample_datapoint(
                "Vehicle.Int64Array", [70, 90, 1440]
            ).value.int64_array.values
        )


@pytest.mark.asyncio
async def test_set_int64_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Int64Array.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.Int64Array.set([1440, 90, 70])
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_uint8():
    vehicle = get_vehicle_instance()

    test_value = 255
    broker_data_point = vehicle.UInt8.create_broker_data_point(test_value)
    assert broker_data_point.value.HasField("uint32")
    assert broker_data_point.value.uint32 == test_value


@pytest.mark.asyncio
async def test_get_uint8():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt8.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.UInt8.get()
        assert response.value == get_sample_datapoint("Vehicle.UInt8", 90).value.uint32


@pytest.mark.asyncio
async def test_set_uint8():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt8.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.UInt8.set(99)
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_uint8_array():
    vehicle = get_vehicle_instance()

    expected_array = [0, 255]
    broker_data_point = vehicle.UInt8Array.create_broker_data_point(expected_array)

    assert broker_data_point.value.HasField("uint32_array")
    actual_array = broker_data_point.value.uint32_array.values
    assert len(expected_array) == len(actual_array)
    for expected_value, actual_value in zip(expected_array, actual_array):
        assert expected_value == actual_value


@pytest.mark.asyncio
async def test_get_uint8_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt8Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.UInt8Array.get()
        assert (
            response.value
            == get_sample_datapoint(
                "Vehicle.UInt8Array", [10, 20, 30]
            ).value.uint32_array.values
        )


@pytest.mark.asyncio
async def test_set_uint8_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt8Array.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.UInt8Array.set([40, 20, 10])
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_uint16():
    vehicle = get_vehicle_instance()

    test_value = 65535
    broker_data_point = vehicle.UInt16.create_broker_data_point(test_value)
    assert broker_data_point.value.HasField("uint32")
    assert broker_data_point.value.uint32 == test_value


@pytest.mark.asyncio
async def test_get_uint16():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt16.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.UInt16.get()
        assert (
            response.value == get_sample_datapoint("Vehicle.UInt16", 144).value.uint32
        )


@pytest.mark.asyncio
async def test_set_uint16():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt16.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.UInt16.set(188)
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_uint16_array():
    vehicle = get_vehicle_instance()

    expected_array = [0, 65535]
    broker_data_point = vehicle.UInt16Array.create_broker_data_point(expected_array)

    assert broker_data_point.value.HasField("uint32_array")
    actual_array = broker_data_point.value.uint32_array.values
    assert len(expected_array) == len(actual_array)
    for expected_value, actual_value in zip(expected_array, actual_array):
        assert expected_value == actual_value


@pytest.mark.asyncio
async def test_get_uint16_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt16Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.UInt16Array.get()
        assert (
            response.value
            == get_sample_datapoint(
                "Vehicle.UInt16Array", [30, 40, 50]
            ).value.uint32_array.values
        )


@pytest.mark.asyncio
async def test_set_uint16_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt16Array.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.UInt16Array.set([300, 400, 500])
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_uint32():
    vehicle = get_vehicle_instance()

    test_value = 4294967295
    broker_data_point = vehicle.UInt32.create_broker_data_point(test_value)
    assert broker_data_point.value.HasField("uint32")
    assert broker_data_point.value.uint32 == test_value


@pytest.mark.asyncio
async def test_get_uint32():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt32.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.UInt32.get()
        assert (
            response.value == get_sample_datapoint("Vehicle.UInt32", 234).value.uint32
        )


@pytest.mark.asyncio
async def test_set_uint32():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt32.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.UInt32.set(2345)
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_uint32_array():
    vehicle = get_vehicle_instance()

    expected_array = [0, 4294967295]
    broker_data_point = vehicle.UInt32Array.create_broker_data_point(expected_array)

    assert broker_data_point.value.HasField("uint32_array")
    actual_array = broker_data_point.value.uint32_array.values
    assert len(expected_array) == len(actual_array)
    for expected_value, actual_value in zip(expected_array, actual_array):
        assert expected_value == actual_value


@pytest.mark.asyncio
async def test_get_uint32_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt32Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.UInt32Array.get()
        assert (
            response.value
            == get_sample_datapoint(
                "Vehicle.UInt32Array", [81, 91, 101]
            ).value.uint32_array.values
        )


@pytest.mark.asyncio
async def test_set_uint32_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt32Array.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.UInt32Array.set([101, 102, 103])
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_uint64():
    vehicle = get_vehicle_instance()

    test_value = 18446744073709551615
    broker_data_point = vehicle.UInt64.create_broker_data_point(test_value)
    assert broker_data_point.value.HasField("uint64")
    assert broker_data_point.value.uint64 == test_value


@pytest.mark.asyncio
async def test_get_uint64():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt64.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.UInt64.get()
        assert (
            response.value == get_sample_datapoint("Vehicle.UInt64", 324).value.uint64
        )


@pytest.mark.asyncio
async def test_set_uint64():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt64.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.UInt64.set(423)
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_uint64_array():
    vehicle = get_vehicle_instance()

    expected_array = [0, 18446744073709551615]
    broker_data_point = vehicle.UInt64Array.create_broker_data_point(expected_array)

    assert broker_data_point.value.HasField("uint64_array")
    actual_array = broker_data_point.value.uint64_array.values
    assert len(expected_array) == len(actual_array)
    for expected_value, actual_value in zip(expected_array, actual_array):
        assert expected_value == actual_value


@pytest.mark.asyncio
async def test_get_uint64_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt64Array.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.UInt64Array.get()
        assert (
            response.value
            == get_sample_datapoint(
                "Vehicle.UInt64Array", [981, 971, 961]
            ).value.uint64_array.values
        )


@pytest.mark.asyncio
async def test_set_uint64_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.UInt64Array.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.UInt64Array.set([100, 200, 300])
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_float():
    vehicle = get_vehicle_instance()

    test_value = 0.75
    broker_data_point = vehicle.Float.create_broker_data_point(test_value)
    assert broker_data_point.value.HasField("float")
    assert broker_data_point.value.float == test_value


@pytest.mark.asyncio
async def test_get_float():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Float.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.Float.get()
        assert (
            response.value
            == get_sample_datapoint("Vehicle.Float", 321.0987).value.float
        )


@pytest.mark.asyncio
async def test_set_float():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Float.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.Float.set(423.123)
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_float_array():
    vehicle = get_vehicle_instance()

    expected_array = [-0.125, 0.875]
    broker_data_point = vehicle.FloatArray.create_broker_data_point(expected_array)

    assert broker_data_point.value.HasField("float_array")
    actual_array = broker_data_point.value.float_array.values
    assert len(expected_array) == len(actual_array)
    for expected_value, actual_value in zip(expected_array, actual_array):
        assert expected_value == actual_value


@pytest.mark.asyncio
async def test_get_float_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.FloatArray.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.FloatArray.get()
        assert (
            response.value
            == get_sample_datapoint(
                "Vehicle.FloatArray", [32.888, 67.9810, 124.67895]
            ).value.float_array.values
        )


@pytest.mark.asyncio
async def test_set_float_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.FloatArray.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.FloatArray.set([423.123, 1.1, 2.2])
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_double():
    vehicle = get_vehicle_instance()

    test_value = 2.718281828459
    broker_data_point = vehicle.Double.create_broker_data_point(test_value)
    assert broker_data_point.value.HasField("double")
    assert broker_data_point.value.double == test_value


@pytest.mark.asyncio
async def test_get_double():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Double.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.Double.get()
        assert (
            response.value
            == get_sample_datapoint("Vehicle.Double", 45678.98765).value.double
        )


@pytest.mark.asyncio
async def test_set_double():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.Double.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.Double.set(98765.123)
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


def test_create_double_array():
    vehicle = get_vehicle_instance()

    expected_array = [2.718281828459, 3.141592653589]
    broker_data_point = vehicle.DoubleArray.create_broker_data_point(expected_array)

    assert broker_data_point.value.HasField("double_array")
    actual_array = broker_data_point.value.double_array.values
    assert len(expected_array) == len(actual_array)
    for expected_value, actual_value in zip(expected_array, actual_array):
        assert expected_value == actual_value


@pytest.mark.asyncio
async def test_get_double_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.DoubleArray.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields("all"),
    ):
        response = await vehicle.DoubleArray.get()
        assert (
            response.value
            == get_sample_datapoint(
                "Vehicle.DoubleArray", [32.456789, 90.1234567, 100.01]
            ).value.double_array.values
        )


@pytest.mark.asyncio
async def test_set_double_array():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.DoubleArray.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ):
        try:
            await vehicle.DoubleArray.set([321.456789, 190.1234567, 1100.01])
        except TypeError as error:
            TestCase.fail(
                False, f"datapoint.set(new_value) raised an exception {error}"
            )


@pytest.mark.asyncio
async def test_unsubscribe():
    vehicle = get_vehicle_instance()
    with mock.patch.object(
        vehicle.Speed.get_client(),
        "Subscribe",
        return_value=AsyncIter([SubscribeResponse(entries=get_fields())]),
    ):
        mock_cb = mock.AsyncMock()
        subscription = await vehicle.Speed.subscribe(mock_cb)

        task = await subscription.unsubscribe()
        assert task.cancelled()


@pytest.mark.asyncio
async def test_subscribe():
    vehicle = get_vehicle_instance()
    with mock.patch.object(
        vehicle.Speed.get_client(),
        "Subscribe",
        return_value=AsyncIter([SubscribeResponse(entries=get_fields())]),
    ):
        mock_cb = mock.Mock()
        subscription = await vehicle.Speed.subscribe(mock_cb)
        assert subscription is not None

        await asyncio.sleep(0)  # Give chance to run subscription

        mock_cb.assert_called_once()
        reply: DataPointReply = mock_cb.call_args_list[0][0][0]
        assert (
            reply.get(vehicle.Speed).value == get_sample_datapoint("Speed").value.float
        )


@pytest.mark.asyncio
async def test_subscribe_with_join():
    vehicle = get_vehicle_instance()
    with mock.patch.object(
        vehicle.Speed.get_client(),
        "Subscribe",
        return_value=AsyncIter([SubscribeResponse(entries=get_fields("JOIN"))]),
    ):
        mock_cb = mock.Mock()
        subscription = await vehicle.Speed.join(
            vehicle.Cabin.Seat.Row1.DriverSide.Position
        ).subscribe(mock_cb)
        assert subscription is not None

        await asyncio.sleep(0)  # Give chance to run subscription

        mock_cb.assert_called_once()
        reply: DataPointReply = mock_cb.call_args_list[0][0][0]
        assert (
            reply.get(vehicle.Speed).value == get_sample_datapoint("Speed").value.float
        )
        assert (
            reply.get(vehicle.Cabin.Seat.Row1.DriverSide.Position).value
            == get_sample_datapoint("Position").value.int32
        )


async def test_get():
    vehicle = get_vehicle_instance()
    with mock.patch.object(
        vehicle.Speed.get_client(),
        "GetDatapoints",
        new_callable=mock.AsyncMock,
        return_value=get_fields(),
    ):
        response = await vehicle.Speed.get()
        assert response.value == get_sample_datapoint("Speed").value.float


@pytest.mark.asyncio
async def test_join():
    vehicle = get_vehicle_instance()
    query = (
        vehicle.Cabin.Seat.Row1.PassengerSide.Position.join(
            vehicle.Speed, vehicle.Cabin.DriverPosition
        )
        .join(vehicle.Speed)
        .get_query()
    )
    expected_path = (
        "SELECT Vehicle.Cabin.Seat.Row1.PassengerSide.Position, Vehicle.Speed, "
        "Vehicle.Cabin.DriverPosition, Vehicle.Speed"
    )
    assert query == expected_path


def test_path_depth2():
    vehicle = get_vehicle_instance()
    path = vehicle.Speed.get_path()
    assert path == "Vehicle.Speed"


def test_path_depth3():
    vehicle = get_vehicle_instance()
    path = vehicle.Cabin.DriverPosition.get_path()
    assert path == "Vehicle.Cabin.DriverPosition"


@pytest.mark.asyncio
async def test_setting_multiple_data_points_atomically():
    vehicle = get_vehicle_instance()

    with mock.patch.object(
        vehicle.get_client(),
        "SetDatapoints",
        new_callable=mock.AsyncMock,
    ) as mock_set_dps:
        (
            await vehicle.set_many()
            .add(vehicle.Bool, False)
            .add(vehicle.StringArray, ["Huhu", "Sarah"])
            .apply()
        )

        bool_data_point = vehicle.Bool.create_broker_data_point(False)
        string_array = vehicle.StringArray.create_broker_data_point(["Huhu", "Sarah"])
        mock_set_dps.assert_called_once_with(
            {
                vehicle.Bool.get_path(): bool_data_point,
                vehicle.StringArray.get_path(): string_array,
            }
        )


@pytest.mark.asyncio
async def test_fail_setting_multiple_data_points_atomically():
    vehicle = get_vehicle_instance()

    with (
        mock.patch.object(
            vehicle.get_client(),
            "SetDatapoints",
            new_callable=mock.AsyncMock,
            side_effect=grpc.aio.AioRpcError(grpc.StatusCode.NOT_FOUND, "", ""),
        ),
        pytest.raises(grpc.aio.AioRpcError),
    ):
        (
            await vehicle.set_many()
            .add(vehicle.Bool, False)
            .add(vehicle.String, "Huhu")
            .apply()
        )


@pytest.mark.asyncio
async def test_get_node__available():
    vehicle = get_vehicle_instance()
    assert vehicle.getNode(vehicle.Speed.get_path()) == vehicle.Speed


@pytest.mark.asyncio
async def test_get_node__not_available():
    vehicle = get_vehicle_instance()
    with pytest.raises(AttributeError):
        vehicle.getNode("Vehicle.NotAvailable")


@pytest.mark.asyncio
async def test_get_node__root_not_in_string():
    vehicle = get_vehicle_instance()
    with pytest.raises(ValueError):
        vehicle.getNode("Speed")


class AsyncIter:
    """AsyncIter"""

    def __init__(self, items: list):
        self.items = items

    def __aiter__(self):
        return self

    async def __anext__(self):
        if len(self.items) > 0:
            return self.items.pop(0)
        # Break endless subscription loop
        raise grpc.aio.AioRpcError(code=grpc.StatusCode.INVALID_ARGUMENT)


def get_fields(condition=""):
    data = {}
    if condition == "":
        data["Vehicle.Speed"] = get_sample_datapoint("Speed")
    elif condition == "JOIN":
        data["Vehicle.Speed"] = get_sample_datapoint("Speed")
        data["Vehicle.Cabin.Seat.Row1.DriverSide.Position"] = get_sample_datapoint(
            "Position"
        )
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
        data["Vehicle.Speed"] = get_sample_datapoint("Speed")
        data["Vehicle.Cabin.Seat.Row1.DriverSide.Position"] = get_sample_datapoint(
            "Position"
        )

    return data


def get_sample_datapoint(data, value=10) -> BrokerDatapoint:
    datapoint = BrokerDatapoint()
    if data == "Speed":
        datapoint.value.float = float(value)
    if data == "Position":
        datapoint.value.int32 = int(value)
    if data == "Vehicle.String":
        datapoint.value.string = str(value)
    if data == "Vehicle.Bool":
        datapoint.value.bool = value
    if data == "Vehicle.Float":
        datapoint.value.float = value
    if data in ["Vehicle.Int8", "Vehicle.Int16", "Vehicle.Int32"]:
        datapoint.value.int32 = value
    if data == "Vehicle.Int64":
        datapoint.value.int64 = value
    if data in ["Vehicle.UInt8", "Vehicle.UInt16", "Vehicle.UInt32"]:
        datapoint.value.uint32 = value
    if data == "Vehicle.UInt64":
        datapoint.value.uint64 = value
    if data == "Vehicle.Double":
        datapoint.value.double = value
    if data == "Vehicle.StringArray":
        datapoint.value.string_array.values.extend(value)
    if data == "Vehicle.BoolArray":
        datapoint.value.bool_array.values.extend(value)
    if data in ["Vehicle.Int8Array", "Vehicle.Int16Array", "Vehicle.Int32Array"]:
        datapoint.value.int32_array.values.extend(value)
    if data == "Vehicle.Int64Array":
        datapoint.value.int64_array.values.extend(value)
    if data in ["Vehicle.UInt8Array", "Vehicle.UInt16Array", "Vehicle.UInt32Array"]:
        datapoint.value.uint32_array.values.extend(value)
    if data == "Vehicle.UInt64Array":
        datapoint.value.uint64_array.values.extend(value)
    if data == "Vehicle.DoubleArray":
        datapoint.value.double_array.values.extend(value)
    return datapoint


def get_vehicle_instance():
    class DriverSide(Model):
        """Seat Instance Class"""

        def __init__(self, parent):
            super().__init__(parent)
            self.Position = DataPointInt32("Position", self)

    class PassengerSide(Model):
        """Seat Instance Class"""

        def __init__(self, parent):
            super().__init__(parent)
            self.Position = DataPointInt32("Position", self)

    class Row1(Model):
        def __init__(self, parent):
            super().__init__(parent)
            self.DriverSide = DriverSide(self)
            self.PassengerSide = PassengerSide(self)

    class Seat(Model):
        """Seat Class"""

        def __init__(self, parent):
            super().__init__(parent)
            self.Row1 = Row1(self)

    class Cabin(Model):
        """Cabin Class"""

        def __init__(self, parent):
            super().__init__(parent)
            self.DriverPosition = DataPointBoolean("DriverPosition", self)
            self.Seat = Seat(self)

    class Vehicle(Model):
        """Mock Class"""

        def __init__(self):
            super().__init__()
            self.Speed = DataPointFloat("Speed", self)
            self.Cabin = Cabin(self)
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

    vehicle = Vehicle()
    # vehicle.get_client()
    return vehicle
