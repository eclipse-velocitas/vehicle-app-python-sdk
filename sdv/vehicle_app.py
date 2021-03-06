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

""" This module contains the Vehicle App base class. """

import asyncio
import inspect
import logging

from sdv import conf
from sdv.vdb.client import VehicleDataBrokerClient
from sdv.vdb.subscriptions import SubscriptionManager, VdbSubscription

from .dapr.client import publish_mqtt_event, wait_for_sidecar
from .dapr.server import register_topic, run_server

logger = logging.getLogger(__name__)


def subscribe_topic(topic: str):
    """Annotation to subscribe to a MQTT topic.

    Args:
        topic ([str]): name of the MQTT topic to subscribe to.
    """

    def wrap(func):
        func.subscribeTopic = topic
        return func

    return wrap


def subscribe_data_points(data_point_names: str, condition: str = None):
    """Annotation to subscribe to one or more data points provided by the vehicle data broker.

    Args:
        data_point_names (str): comma-separate list of data point names to subscribe to.
        condition (str, optional): condition to apply to the data points. Defaults to None.
    """
    query = "SELECT " + data_point_names

    if condition is not None:
        query += " WHERE " + condition

    def wrap(func):
        func.subscribeDataPoints = query
        return func

    return wrap


class VehicleApp:
    """Vehicle App base class. All Vehicle Apps must inherit from this class"""

    def __init__(self):
        self._vdb_client = VehicleDataBrokerClient()
        logger.debug("Talent instantiation successfully done")

    async def on_start(self):
        """Override to add additional initialization code on startup, like
        - adding subscriptions to vehicle data broker
        """

    async def stop(self) -> None:
        """Stop the Vehicle App"""
        await SubscriptionManager.remove_all_subscriptions()
        await self._vdb_client.close()

    async def run(self):
        """Run the Vehicle App"""
        methods = inspect.getmembers(self)
        if not conf.DISABLE_DAPR:
            await run_server()
            # dapr requires to subscribe to pubsub topics during sidecar initialization
            for method in methods:
                if hasattr(method[1], "subscribeTopic"):
                    try:
                        register_topic(method[1].subscribeTopic, method[1])
                    except Exception as ex:
                        logger.exception(ex)

            await wait_for_sidecar()

        # register vehicle data broker subscriptions using dapr grpc proxying after dapr
        # is initialized
        for method in methods:
            if hasattr(method[1], "subscribeDataPoints"):
                sub = VdbSubscription(
                    self._vdb_client, method[1].subscribeDataPoints, method[1]
                )
                try:
                    SubscriptionManager._add_subscription(sub)
                except Exception as ex:
                    logger.exception(ex)

        try:
            await self.on_start()
            while True:
                await asyncio.sleep(1)
        except Exception:
            await self.stop()

    async def publish_mqtt_event(self, topic: str, data: str) -> None:
        """Publish an event to the specified MQTT topic"""
        publish_mqtt_event(topic, data)
