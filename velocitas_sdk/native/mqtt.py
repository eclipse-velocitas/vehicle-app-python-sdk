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
import logging
from typing import Optional

import paho.mqtt.client as mqtt  # type: ignore

from velocitas_sdk.base import PubSubClient

logger = logging.getLogger(__name__)


class MqttTopicSubscription:
    """Mqtt topic subscription object that consists of topic and callback."""

    def __init__(self, topic, callback):
        self.topic = topic
        self.callback = callback


class MqttClient(PubSubClient):
    """This class is a wrapper for the on_message callback of the MQTT broker."""

    def __init__(self, port: Optional[int] = None, hostname: Optional[str] = None):
        self._port = port
        self._hostname = hostname
        self._topics_to_subscribe: list[MqttTopicSubscription] = []

        self._pub_client = mqtt.Client()
        self._sub_client = mqtt.Client()
        self._sub_client.on_connect = self.on_connect
        self._sub_client.on_disconnect = self.on_disconnect

        self._sub_client.connect(self._hostname, self._port)
        self._pub_client.connect(self._hostname, self._port)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.debug("Mqtt native connection OK!")

            # subscribe the registered topics
            for subscription in self._topics_to_subscribe:
                client.subscribe(subscription.topic)
        else:
            logger.error("Bad connection request, return code: %d", rc)

    def on_disconnect(self, client, userdata, rc):
        logger.debug("Mqtt native is disconnected with reason:  %d", rc)

    async def run(self):
        self._sub_client.loop_start()

    async def init(self):
        """Do nothing"""

    async def subscribe_topic(self, topic, coro):
        self._topics_to_subscribe.append(MqttTopicSubscription(topic, coro))
        if self._sub_client.is_connected():
            self._sub_client.subscribe(topic)

        loop = asyncio.get_event_loop()

        @self._sub_client.topic_callback(topic)
        def handle(client, userdata, msg):
            try:
                message = str(msg.payload.decode("utf-8"))
            except UnicodeDecodeError as err:
                logger.error(err)
                return
            if asyncio.iscoroutinefunction(coro):
                # run the async callbacks on the main event loop
                asyncio.run_coroutine_threadsafe(coro(message), loop)
            else:
                coro(message)

    async def publish_event(self, topic: str, data: str):
        return self._pub_client.publish(topic, data)
