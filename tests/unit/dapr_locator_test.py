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

""" Tests for methods in locator """


import os

os.environ["SDV_MIDDLEWARE_TYPE"] = "dapr"

from unittest import mock

import pytest

from sdv import config
from sdv.config import Config
from sdv.dapr.middleware import DaprMiddleware
from sdv.model import Service, VehicleDataBrokerClient


@pytest.fixture(autouse=True)
def reset():
    VehicleDataBrokerClient._instance = None
    config._config = Config("dapr")
    config.middleware = DaprMiddleware()


@pytest.mark.asyncio
async def test_for_get_metadata():
    service = CustomService()
    response = service.metadata
    assert response == (("dapr-app-id", str(service.name).lower()),)


@pytest.mark.asyncio
async def test_for_get_location():
    service = CustomService()
    _address = service.address
    assert _address == "localhost:51001"
    with mock.patch.dict(os.environ, {"DAPR_GRPC_PORT": "55555"}):
        service = CustomService()
        response = service.address
        assert response == "localhost:55555"


class CustomService(Service):
    "Custom model"

    def __init__(self):
        super().__init__()
