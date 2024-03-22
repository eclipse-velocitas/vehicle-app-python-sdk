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

"""Tests for methods in VehicleClient"""

import inspect
from typing import Mapping, Text
from unittest import mock

import pytest

from velocitas_sdk.proto.broker_pb2 import SubscribeReply
from velocitas_sdk.proto.types_pb2 import Datapoint
from velocitas_sdk.vehicle_app import VehicleApp, subscribe_data_points


@pytest.mark.asyncio
async def test_publish_event():
    vehicle_app = get_vehicle_app_instance()
    with mock.patch.object(
        vehicle_app,
        "publish_mqtt_event",
        return_value=None,
    ) as mock_publish_mqtt_event:
        await vehicle_app.publish_mqtt_event(
            "seatadjuster/setPosition/request/gui-app",
            '{"position": 300, "requestId": "xyz"}',
        )
        mock_publish_mqtt_event.assert_called()
        await vehicle_app.stop()


def test_subscribe_to_data_points_decorator():
    class DecoratorMock:
        """Mock to check decorator"""

        query = []

        @subscribe_data_points(
            "Vehicle.ADAS.CruiseControl.SpeedSet", "Vehicle.Speed > 0"
        )
        def placeholder_where(self):
            pass

        @subscribe_data_points("Vehicle.ADAS.CruiseControl.SpeedSet")
        def placeholder(self):
            pass

        def getattr(self):
            methods = inspect.getmembers(self)
            for method in methods:
                if hasattr(method[1], "subscribeDataPoints"):
                    self.query.append(method[1].subscribeDataPoints)

            return self.query

    decorator = DecoratorMock()
    query = decorator.getattr()
    assert "SELECT Vehicle.ADAS.CruiseControl.SpeedSet" in query
    assert "SELECT Vehicle.ADAS.CruiseControl.SpeedSet WHERE Vehicle.Speed > 0" in query


# @mock.patch.dict(os.environ, {"DAPR_GRPC_PORT": "50051"}, clear=True)
def get_vehicle_app_instance() -> VehicleApp:
    vehicle_app = VehicleApp()
    return vehicle_app


# Mock data


def get_sample_subscription_reply():
    datapoint = Datapoint()
    datapoint.int32_value = 0
    mapping: Mapping[Text, Datapoint] = {}
    mapping["Vehicle.Speed"] = datapoint

    reply = SubscribeReply(fields=mapping)

    return reply


class AsyncIterator:
    """Async wrapper for subscription reply mocks"""

    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration as ex:
            raise StopAsyncIteration from ex
