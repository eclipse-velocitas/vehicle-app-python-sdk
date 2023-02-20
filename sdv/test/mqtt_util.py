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

# pylint: disable=C0103,W0613

import asyncio
import json
import os
import time
from typing import Optional

import paho.mqtt.client as mqtt  # type: ignore


class SingleMessageCallback:
    """This class is a wrapper for the on_message callback of the MQTT broker.
    It waits for the first message to arrive."""

    def __init__(self):
        self.message: str = ""

    def __call__(self, client: mqtt.Client, userdata, message):
        self.message = str(message.payload.decode("utf-8"))


class PropertyWatcherCallback:
    """This class monitors a topic for incoming message and checks, if a specific
    property has the correct value"""

    def __init__(self, path, value):
        self.__path = path
        self.__value = value
        self.message: str = ""

    def __call__(self, client, userdata, message):
        payload_str = str(message.payload.decode("utf-8"))
        payload = json.loads(payload_str)

        value = payload
        for part in self.__path:
            value = value[part]
            if value == self.__value:
                self.message = payload_str
                break


class MqttClient:
    """This class is a wrapper for the on_message callback of the MQTT broker."""

    def __init__(self, port: Optional[int] = None):
        if port is None:
            value = os.getenv("MQTT_PORT")

            if value is not None:
                port = int(str(value))

        if port is None:
            port = 1883  # default port of MQTT Broker when running locally

        self._port = port
        self._hostname = "localhost"

    def create_and_connect_mqtt_client(self, callback) -> mqtt.Client:
        client = mqtt.Client()
        client.on_message = callback
        client.connect(self._hostname, self._port)
        return client

    def create_client(self):
        client = mqtt.Client()
        client.connect_async(self._hostname, self._port)
        return client

    def on_connect_callback(self, client, topic, coro):
        @client.connect_callback()
        def on_connect(client, userdata, flags, rc):
            client.subscribe(topic)

        loop = asyncio.get_event_loop()

        @client.topic_callback(topic)
        def handle(client, userdata, msg):
            message = str(msg.payload.decode("utf-8"))
            if asyncio.iscoroutinefunction(coro):
                # run the async callbacks on the main event loop
                asyncio.run_coroutine_threadsafe(coro(message), loop)
            else:
                coro(message)

    def publish_and_wait_for_response(
        self, request_topic: str, response_topic: str, payload, timeout: int = 20000
    ) -> str:
        callback = SingleMessageCallback()
        client = self.create_and_connect_mqtt_client(callback)

        counter = 0
        interval = 100

        client.subscribe(response_topic)

        client.loop_start()

        client.publish(request_topic, json.dumps(payload))

        while callback.message == "" and counter < timeout:
            counter += interval
            time.sleep(interval / 1000)

        client.loop_stop()

        return callback.message

    def publish_and_wait_for_property(
        self,
        request_topic: str,
        response_topic: str,
        payload,
        path,
        value,
        timeout: int = 20000,
    ) -> str:
        callback = PropertyWatcherCallback(path, value)
        client = self.create_and_connect_mqtt_client(callback)

        counter = 0
        interval = 100

        client.subscribe(response_topic)

        client.loop_start()

        client.publish(request_topic, json.dumps(payload))

        while callback.message == "" and counter < timeout:
            counter += interval
            time.sleep(interval / 1000)

        client.loop_stop()

        return callback.message
