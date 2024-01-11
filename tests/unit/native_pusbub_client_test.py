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

""" Tests for methods in PubSubClient """
import os
import time

os.environ["SDV_MIDDLEWARE_TYPE"] = "native"

import sys
from unittest import mock

import pytest

from velocitas_sdk import config
from velocitas_sdk.base import Middleware
from velocitas_sdk.config import Config
from velocitas_sdk.native.mqtt import MqttClient

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))


@pytest.fixture(autouse=True)
def reset():
    config._config = Config("native")
    config.middleware = config._config.middleware


@pytest.mark.asyncio
async def test_for_subscribe_topic():
    middleware = get_middleware_instance()
    with mock.patch.object(
        middleware.pubsub_client,
        "subscribe_topic",
        new_callable=mock.AsyncMock,
    ) as mocked_client:
        await middleware.pubsub_client.subscribe_topic("/test/native", None)
        assert isinstance(middleware.pubsub_client, MqttClient)
        mocked_client.assert_called_once_with("/test/native", None)


@pytest.mark.asyncio
async def test_for_get_publish_event():
    middleware = get_middleware_instance()
    with mock.patch.object(
        middleware.pubsub_client,
        "publish_event",
        new_callable=mock.AsyncMock,
    ) as mocked_client:
        await middleware.pubsub_client.publish_event("/test/native", "message")
        mocked_client.assert_called_once_with("/test/native", "message")


@pytest.mark.asyncio
async def test_for_subscribe_mqtt_event():
    middleware = get_middleware_instance()
    mqtt_client = middleware.pubsub_client
    callback = CallbackClass()
    await middleware.start()
    await mqtt_client.run()
    await mqtt_client.subscribe_topic("test/test_subscribe", callback)
    # wait a moment to really subscribe
    time.sleep(0.5)
    await mqtt_client.publish_event("test/test_subscribe", "test")

    time.sleep(1)
    assert callback.executed


@pytest.mark.asyncio
async def test_for_error_message():
    middleware = get_middleware_instance()
    mqtt_client = middleware.pubsub_client
    callback = CallbackClass()
    await middleware.start()
    await mqtt_client.run()
    await mqtt_client.subscribe_topic("test/test_error", callback)
    # wait a moment to really subscribe
    time.sleep(0.5)
    await mqtt_client.publish_event("test/test_error", b"\xc3")
    assert not callback.executed


def get_middleware_instance() -> Middleware:
    return config.middleware


class CallbackClass:
    def __init__(self):
        self.executed = False

    def __call__(self, message):
        self.executed = True
