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

from sdv.test.mqtt_util import MqttClient


def test_create_and_connect_mqtt_client():
    mqtt_client = get_mqtt_client_instance()

    payload = {"position": 300, "requestId": "abc"}

    with mock.patch.object(
        mqtt_client,
        "create_and_connect_mqtt_client",
        new_callable=mock.PropertyMock,
    ):
        message = mqtt_client.publish_and_wait_for_response(
            request_topic=pytest.request_topic,
            response_topic=pytest.response_topic,
            payload=payload,
            timeout=100,
        )

        assert message == ""


def test_publish_and_wait_for_property():
    mqtt_client = get_mqtt_client_instance()

    payload = {"position": 300, "requestId": "abc"}

    with mock.patch.object(
        mqtt_client,
        "create_and_connect_mqtt_client",
        new_callable=mock.PropertyMock,
    ):
        position = 200
        payload = {"position": position, "requestId": "abc"}

        response = mqtt_client.publish_and_wait_for_property(
            request_topic=pytest.request_topic,
            response_topic="seatadjuster/currentPosition",
            payload=payload,
            path=["position"],
            value=position,
            timeout=100,
        )

        assert response == ""


@pytest.fixture(scope="session", autouse=True)
def pytest_configure():
    pytest.request_topic = "seatadjuster/setPosition/request"
    pytest.response_topic = "seatadjuster/setPosition/response"


def get_mqtt_client_instance():
    client = MqttClient()
    return client
