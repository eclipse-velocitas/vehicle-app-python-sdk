import asyncio
import os
from typing import Optional

import paho.mqtt.client as mqtt  # type: ignore


class MqttTopicSubscription:
    def __init__(self, topic, callback):
        self.topic = topic
        self.callback = callback


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

    def register_topic(self, topic, coro):
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

    def publish_event(self, topic: str, data: str) -> None:
        self._pub_client.publish(topic, data)
