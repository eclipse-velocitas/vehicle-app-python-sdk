# Copyright (c) 2022-2023 Robert Bosch GmbH and Microsoft Corporation
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


# Disable name checks due to proto generated classes
# pylint: disable=C0103,W0631

""" Tests for methods in VehicleDataBrokerClient """

import os

import pytest

os.environ["SDV_MIDDLEWARE_TYPE"] = "dapr"

from sdv import config
from sdv.test.databroker_testhelper import Vehicle, vehicle
from sdv.vdb.client import VehicleDataBrokerClient
from sdv.vehicle_app import VehicleApp


@pytest.fixture(autouse=True)
def reset():
    VehicleDataBrokerClient._instance = None
    config._config = None


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
