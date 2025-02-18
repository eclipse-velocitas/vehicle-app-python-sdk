# Copyright (c) 2022-2025 Contributors to the Eclipse Foundation
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

""" Tests for methods in locator """


import os
from unittest import mock

import pytest

from velocitas_sdk import config
from velocitas_sdk.config import Config
from velocitas_sdk.model import Service, VehicleDataBrokerClient
from velocitas_sdk.native.middleware import NativeMiddleware


@pytest.fixture(autouse=True)
def reset():
    os.environ["SDV_MIDDLEWARE_TYPE"] = "native"
    os.environ["SDV_MQTT_ADDRESS"] = "mqtt://localhost:1883"
    os.environ["SDV_VEHICLEDATABROKER_ADDRESS"] = "grpc://localhost:55555"
    os.environ["SDV_CUSTOMSERVICE_ADDRESS"] = "grpc://localhost:51001"

    VehicleDataBrokerClient._instance = None
    config._config = Config("native")
    config.middleware = NativeMiddleware()


@pytest.mark.asyncio
async def test_for_get_metadata():
    service = CustomService()
    response = service.metadata
    assert response is None


@pytest.mark.asyncio
async def test_for_get_location():
    service = CustomService()
    _address = service.address
    assert _address == "localhost:51001"
    with mock.patch.dict(
        os.environ, {"SDV_CUSTOMSERVICE_ADDRESS": "grpc://localhost:51555"}
    ):
        service = CustomService()
        response = service.address
        assert response == "localhost:51555"


class CustomService(Service):
    "Custom model"

    def __init__(self):
        super().__init__()
