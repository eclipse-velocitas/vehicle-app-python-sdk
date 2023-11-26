# Copyright (c) 2022-2023 Contributors to the Eclipse Foundation
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

""" Tests for methods in PubSubClient """
import os

os.environ["SDV_MIDDLEWARE_TYPE"] = "dapr"

import sys
from unittest import mock

import pytest

from velocitas_sdk import config
from velocitas_sdk.base import Middleware
from velocitas_sdk.config import Config
from velocitas_sdk.dapr.pubsub import DaprClient

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))


@pytest.fixture(autouse=True)
def reset():
    config._config = Config("dapr")
    config.middleware = config._config.middleware


@pytest.mark.asyncio
async def test_for_subscribe_topic():
    middleware = get_middleware_instance()
    with mock.patch.object(
        middleware.pubsub_client,
        "subscribe_topic",
        new_callable=mock.AsyncMock,
    ) as mocked_client:
        await middleware.pubsub_client.subscribe_topic("/test/dapr", None)
        assert isinstance(middleware.pubsub_client, DaprClient)
        mocked_client.assert_called_once_with("/test/dapr", None)


@pytest.mark.asyncio
async def test_for_get_publish_event():
    middleware = get_middleware_instance()
    with mock.patch.object(
        middleware.pubsub_client,
        "publish_event",
        new_callable=mock.AsyncMock,
    ) as mocked_client:
        await middleware.pubsub_client.publish_event("/test/dapr", "message")
        mocked_client.assert_called_once_with("/test/dapr", "message")


def get_middleware_instance() -> Middleware:
    return config.middleware
