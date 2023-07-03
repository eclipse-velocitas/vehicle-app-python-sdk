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

from unittest import mock

import pytest
from vehicle import vehicle  # type: ignore

from sdv.vehicle_app import VehicleApp


@pytest.mark.asyncio
async def test_for_set_position_request_received():
    with mock.patch.object(
        vehicle.Cabin.Seat.Row1.Pos1.Position,
        "set",
        new_callable=mock.AsyncMock,
        return_value=get_sample_response(),
    ):
        get_position = get_sample_request_data()
        response = await vehicle.Cabin.Seat.Row1.Pos1.Position.set(
            get_position["position"]
        )
        assert response == get_sample_response()


@pytest.mark.asyncio
async def test_for_set_position_request_received_high_position():
    with mock.patch.object(
        vehicle.Cabin.Seat.Row1.Pos1.Position,
        "set",
        new_callable=mock.AsyncMock,
        return_value=get_error_invalid_arg_response(),
    ):
        set_position = set_seat_position_high()
        response = await vehicle.Cabin.Seat.Row1.Pos1.Position.set(
            set_position["position"]
        )
        assert response == get_error_invalid_arg_response()


@pytest.mark.asyncio
async def test_for_set_position_request_received_error_path():
    with mock.patch.object(
        vehicle.Cabin.Seat.Row1.Pos1.Position,
        "set",
        new_callable=mock.AsyncMock,
        return_value=get_error_response(),
    ):
        get_position = get_sample_request_data()
        response = await vehicle.Cabin.Seat.Row1.Pos1.Position.set(
            get_position["position"]
        )
        assert response == get_error_response()


@pytest.mark.asyncio
async def test_for_publish_to_topic():
    with mock.patch.object(
        VehicleApp, "publish_mqtt_event", new_callable=mock.AsyncMock, return_value=-1
    ):
        response = await VehicleApp.publish_mqtt_event(
            str("sampleTopic"), get_sample_request_data()  # type: ignore
        )
        assert response == -1


def get_sample_request_data():
    return {"position": 330, "requestId": 123456789}


def set_seat_position_high():
    return {"position": 1001, "requestId": 123456789}


def get_error_invalid_arg_response():
    data = set_seat_position_high()
    error_msg = f"""Provided position {data["position"]}  \
        should not be Greater than 1000 (Max)"""
    resp_data = {
        "requestId": data["requestId"],
        "result": {"status": 1, "message": error_msg},
    }
    return resp_data


def get_sample_response():
    get_position = get_sample_request_data()
    resp_data = {
        "requestId": {
            "requestId": get_position["requestId"],
            "result": {
                "status": 0,
                "message": f"Set Seat position to: {get_position['position']}",
            },
        }
    }
    return resp_data


def get_error_response():
    data = get_sample_request_data()
    error_msg = "Received unknown RPC error"
    resp_data = {
        "requestId": data["requestId"],
        "result": {"status": 1, "message": error_msg},
    }
    return resp_data
