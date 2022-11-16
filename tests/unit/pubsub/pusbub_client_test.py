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

""" Tests for methods in PubSubClient """
import os
import sys
from unittest import mock

import pytest

from sdv import conf
from sdv.pubsub.client import PubSubClient
from sdv.pubsub.dapr import DaprClient
from sdv.pubsub.mqtt import MqttClient

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))


@pytest.mark.asyncio
async def test_for_subscribe_topic():
    conf.DISABLE_DAPR = True

    client = get_pubsub_client_instance()
    with mock.patch.object(
        client.native_client,
        "register_topic",
        new_callable=mock.AsyncMock,
    ) as mocked_client:
        await client.subscribe_topic("/test/native", None)
        assert isinstance(client.native_client, MqttClient)
        mocked_client.assert_called_once_with("/test/native", None)

    conf.DISABLE_DAPR = False
    client = get_pubsub_client_instance()
    with mock.patch.object(
        client.native_client,
        "register_topic",
        new_callable=mock.AsyncMock,
    ) as mocked_client:
        await client.subscribe_topic("/test/dapr", None)
        assert isinstance(client.native_client, DaprClient)
        mocked_client.assert_called_once_with("/test/dapr", None)


@pytest.mark.asyncio
async def test_for_get_publish_event():
    conf.DISABLE_DAPR = True

    client = get_pubsub_client_instance()
    with mock.patch.object(
        client.native_client,
        "publish_event",
        new_callable=mock.AsyncMock,
    ) as mocked_client:
        await client.publish_event("/test/native", "message")
        mocked_client.assert_called_once_with("/test/native", "message")


def get_pubsub_client_instance() -> PubSubClient:
    client = PubSubClient()
    return client
