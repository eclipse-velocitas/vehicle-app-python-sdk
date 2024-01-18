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

""" Tests for methods in VehicleDataBrokerClient """

import pytest

from velocitas_sdk import config
from velocitas_sdk.test.databroker_testhelper import Vehicle, vehicle
from velocitas_sdk.vdb.client import VehicleDataBrokerClient
from velocitas_sdk.vehicle_app import VehicleApp


@pytest.fixture(autouse=True)
def reset():
    config._config = None
    VehicleDataBrokerClient._instance = None


@pytest.mark.asyncio
async def test_for_publish_mqtt_event():
    mqtt_client = get_vehicleapp_instance().pubsub_client
    await mqtt_client.publish_event("test/test_for_publish_mqtt_event", "test")
    assert True


class TestPubSubVehicleApp(VehicleApp):
    def __init__(self, vehicle_client: Vehicle):
        super().__init__()
        self.Vehicle = vehicle_client


def get_vehicleapp_instance():
    app = TestPubSubVehicleApp(vehicle)
    return app
