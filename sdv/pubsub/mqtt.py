import asyncio
import os
from typing import Optional

import paho.mqtt.client as mqtt  # type: ignore


class MqttClient:
    """This class is a wrapper for the on_message callback of the MQTT broker."""

    def __init__(self, port: Optional[int] = None, hostname: Optional[str] = None):
        if port is None:
            value = os.getenv("SDV_MQTT_PORT", "1883")
            port = int(str(value))

        if hostname is None:
            hostname = os.getenv("SDV_MQTT_HOSTNAME", "localhost")

        self._port = port
        self._hostname = hostname
        self._pub_client = self.__create_client()
        self._sub_client = self.__create_client()

    def __create_client(self):
        client = mqtt.Client()
        client.connect_async(self._hostname, self._port)
        return client

    def __on_connect_callback(self, client, topic, coro):
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

    async def register_topic(self, topic, coro):
        self.__on_connect_callback(self._sub_client, topic, coro)

    def publish_event(self, topic: str, data: str) -> None:
        self._pub_client.publish(topic, data)
