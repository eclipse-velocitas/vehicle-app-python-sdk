from sdv.pubsub.mqtt import MqttClient
from sdv.pubsub.dapr import DaprClient

import logging
logger = logging.getLogger(__name__)

from sdv import conf


class PubSubClient:
    """Generic Pub Sub facade"""

    def __init__(self):
        if conf.middleware_type == "native":
            self.native_client = MqttClient()
        else:
            self.native_client = DaprClient()

    async def init(self):
        await self.native_client.init()
        
    async def run(self):
        await self.native_client.run()

    def subscribe_topic(self, topic, coro):
        self.native_client.register_topic(topic, coro)

    async def publish_event(self, topic: str, data: str):
        self.native_client.publish_event(topic, data)
