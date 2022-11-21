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

import asyncio
from typing import Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt  # type: ignore

from sdv.base import PubSubClient
from sdv.native.locator import NativeServiceLocator

_service_locator = NativeServiceLocator()


class MqttTopicSubscription:
    def __init__(self, topic, callback):
        self.topic = topic
        self.callback = callback


class MqttClient(PubSubClient):
    """This class is a wrapper for the on_message callback of the MQTT broker."""

    def __init__(self, port: Optional[int] = None, hostname: Optional[str] = None):
        self._address = _service_locator.get_service_location("mqtt")
        self._port = urlparse(self._address).port
        self._hostname = urlparse(self._address).hostname
        self._pub_client = self.__create_client()
        self._sub_client = self.__create_client()
        self._registered_topics = []

        @self._sub_client.connect_callback()
        def on_connect(client, userdata, flags, rc):
            for subscription in self._registered_topics:
                client.subscribe(subscription.topic)

    def __create_client(self):
        client = mqtt.Client()
        client.connect(self._hostname, self._port)
        return client

    async def run(self):
        self._sub_client.loop_start()

    async def init(self):
        """Do nothing"""

    async def register_topic(self, topic, coro):
        if not self._sub_client.is_connected():
            self._registered_topics.append(MqttTopicSubscription(topic, coro))
        else:
            self._sub_client.subscribe(topic)

        loop = asyncio.get_event_loop()

        @self._sub_client.topic_callback(topic)
        def handle(client, userdata, msg):
            message = str(msg.payload.decode("utf-8"))
            if asyncio.iscoroutinefunction(coro):
                # run the async callbacks on the main event loop
                asyncio.run_coroutine_threadsafe(coro(message), loop)
            else:
                coro(message)

        # self.__on_connect_callback(self._sub_client, topic, coro)

    async def publish_event(self, topic: str, data: str):
        return self._pub_client.publish(topic, data)
