from sdv.pubsub.mqtt import MqttClient
from sdv.pubsub.dapr import DaprClient
from sdv.pubsub.chariott import ChariottPubSubClient
from sdv import conf
import logging
logger = logging.getLogger(__name__)


class PubSubClient:
    """Generic Pub Sub facade"""

    def __init__(self):
        if conf.middleware_type == "native":
            self.native_client = MqttClient()
        elif conf.middleware_type == "dapr":
            self.native_client = DaprClient()
        else:
            self.native_client = ChariottPubSubClient()

    async def init(self):
        await self.native_client.init()
        
    async def run(self):
        await self.native_client.run()

    def subscribe_topic(self, topic, coro):
        self.native_client.register_topic(topic, coro)

    def publish_event(self, topic: str, data: str) -> None:
        self.native_client.publish_event(topic, data)
