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

# Disable name checks due to proto generated classes
# pylint: disable=C0103,W0631

""" Tests for methods in VehicleDataBrokerClient """

# import os
# from unittest import mock

# import grpc
import pytest

from sdv.base import Config
# from sdv.test.databroker_testhelper import SubscribeException, Vehicle
# from sdv.test.inttesthelper import IntTestHelper
from sdv.vdb.client import VehicleDataBrokerClient
from sdv.vehicle_app import VehicleApp


@pytest.fixture(autouse=True)
def setup_vdb_client():
    VehicleDataBrokerClient._instance = None


@pytest.mark.asyncio
async def test_for_publish_mqtt_event():
    client = get_vehicleapp_instance()
    client.run()
    await client.publish_mqtt_event("test/test_for_publish_mqtt_event", "test")
    assert True


def get_vehicleapp_instance():
    Config().disable_dapr()
    client = VehicleApp()
    return client
