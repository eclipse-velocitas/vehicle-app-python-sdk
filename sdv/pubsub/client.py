from sdv.dapr.client import publish_mqtt_event, wait_for_sidecar
from sdv.dapr.server import register_topic, run_server
from sdv.pubsub.mqtt import MqttClient

import logging
logger = logging.getLogger(__name__)

from sdv import conf


class PubSubClient:
    """Generic Pub Sub facade"""

    def __init__(self):
        if not conf.DISABLE_DAPR:
            self.native_client = MqttClient()

    async def run(self):
        if not conf.DISABLE_DAPR:
            await run_server()
            await wait_for_sidecar()
        else:
            self.sub_cli.loop_start()

    async def subscribe_topic(self, topic, coro):
        if not conf.DISABLE_DAPR:
            self.register_topic_dapr(topic, coro)
        else:
            try:
                self.register_topic_native(topic, coro)
            except Exception as ex:
                logger.exception(ex)

    async def register_topic_dapr(self, topic, coro):
        # dapr requires to subscribe to pubsub topics during sidecar initialization
        try:
            register_topic(topic, coro)
        except Exception as ex:
            logger.exception(ex)

    async def registr_topic_native(self, topic, coro):
        try:
            self.native_client.register_topic(topic, coro)
        except Exception as ex:
            logger.exception(ex)

    async def publish_event(self, topic: str, data: str) -> None:
        """Publish an event to the specified MQTT topic"""
        if conf.DISABLE_DAPR:
            self.native_client.publish_event(topic, data)
        else:
            publish_mqtt_event(topic, data)
