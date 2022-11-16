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

import logging

from sdv.config import Middleware
from sdv.pubsub.dapr import DaprClient
from sdv.pubsub.mqtt import MqttClient

logger = logging.getLogger(__name__)

from sdv import conf


class PubSubClient:
    """Generic Pub Sub facade"""

    def __init__(self):
        if conf.config.middleware_value == Middleware.NATIVE.value:
            self.native_client = MqttClient()
        elif conf.config.middleware_value == Middleware.DAPR.value:
            self.native_client = DaprClient()

    async def init(self):
        await self.native_client.init()

    async def run(self):
        await self.native_client.run()

    def subscribe_topic(self, topic, coro):
        self.native_client.register_topic(topic, coro)

    async def publish_event(self, topic: str, data: str):
        self.native_client.publish_event(topic, data)
