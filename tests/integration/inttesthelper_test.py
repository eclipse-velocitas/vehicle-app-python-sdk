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

""" Tests for methods in VehicleCollectorClient """
import pytest

from sdv.databroker.v1.types_pb2 import DataType
from sdv.test.inttesthelper import IntTestHelper


@pytest.mark.asyncio
async def test_for_registerdatapoint():
    client = get_inttesthelper_instance()
    response = await client.register_datapoint(
        name="Vehicle.Speed", data_type=DataType.FLOAT
    )
    assert isinstance(response, int)


@pytest.mark.asyncio
async def test_for_update_bool_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_bool_datapoint("Vehicle.ThisIsABool", True)
    response = await client.set_bool_datapoint("Vehicle.ThisIsABool", False)
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_boolarray_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_boolArray_datapoint(
        "Vehicle.ThisIsABoolArray", [True, False, True, True, False]
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_double_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_double_datapoint("Vehicle.ThisIsADouble", 50.6020814126)
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_doublearray_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_doubleArray_datapoint(
        "Vehicle.ThisIsADoubleArray", [45.60, 50.6536, 50.6020836, 50.602083526]
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_float_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_float_datapoint("Vehicle.ThisIsAFloat", 50.60208)
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_floatarray_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_floatArray_datapoint(
        "Vehicle.ThisIsAFloatArray", [45.60, 50.6536, 50.6020815, 50.602083526]
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_int8_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_int8_datapoint("Vehicle.ThisIsAnInteger8", 2**31 - 1)
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_int8array_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_int8Array_datapoint(
        "Vehicle.ThisIsAInt8Array", [45, 50, 60, 70, 2**31 - 1]
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_int16_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_int16_datapoint(
        "Vehicle.ThisIsAnInteger16", 2**31 - 1
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_int16array_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_int16Array_datapoint(
        "Vehicle.ThisIsAInt162Array", [45, 50, 60, 70, 2**31 - 1]
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_int32_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_int32_datapoint(
        "Vehicle.ThisIsAnInteger32", 2**31 - 1
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_int32array_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_int32Array_datapoint(
        "Vehicle.ThisIsAInt32Array", [45, 50, 60, 70, 2**31 - 1]
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_int64_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_int64_datapoint(
        "Vehicle.ThisIsAnInteger64", 2**63 - 1
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_int64array_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_int64Array_datapoint(
        "Vehicle.ThisIsAInt64Array", [45, 50, 60, 70, 2**63 - 1]
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_string_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_string_datapoint("Vehicle.ThisIsAString", "example")
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_stringarray_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_stringArray_datapoint(
        "Vehicle.ThisIsAStringArray",
        [
            "abcd12345",
            "singleWord",
            "ALLCAPS",
            "string with spaces",
            "$pec!@l characters",
        ],
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_uint8_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_uint8_datapoint("Vehicle.ThisIsAnUInteger8", 2**30)
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_uint8array_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_uint8Array_datapoint(
        "Vehicle.ThisIsAUInt8Array", [45, 50, 60, 70, 2**30]
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_uint16_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_uint16_datapoint("Vehicle.ThisIsAnUInteger16", 2**30)
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_uint16array_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_uint16Array_datapoint(
        "Vehicle.ThisIsAUInt16Array", [45, 50, 60, 70, 2**30]
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_uint32_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_uint32_datapoint("Vehicle.ThisIsAnUInteger32", 2**30)
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_uint32array_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_uint32Array_datapoint(
        "Vehicle.ThisIsAUInt32Array", [45, 50, 60, 70, 2**30]
    )
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_uint64_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_uint64_datapoint("Vehicle.ThisIsAnUInteger64", 2**60)
    assert len(response.errors) == 0


@pytest.mark.asyncio
async def test_for_update_uint64array_datapoint():
    client = get_inttesthelper_instance()
    response = await client.set_uint64Array_datapoint(
        "Vehicle.ThisIsAUInt64Array", [45, 50, 60, 70, 2**60]
    )
    assert len(response.errors) == 0


def get_inttesthelper_instance():
    client = IntTestHelper()
    return client
