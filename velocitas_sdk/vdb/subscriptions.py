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

import grpc

from velocitas_sdk.vdb.reply import DataPointReply

logger = logging.getLogger(__name__)


class SubscriptionManager:
    """Helper for subscription handling."""

    _subscription_tasks = {}  # type: ignore

    @staticmethod
    async def remove_all_subscriptions():
        for task in SubscriptionManager._subscription_tasks.items():
            try:
                await SubscriptionManager._remove_subscription(task[0])
            except Exception as ex:
                logger.exception(ex)

    @staticmethod
    def list_all_subscription():
        queries = []
        for task in SubscriptionManager._subscription_tasks.items():
            if not (task[1].cancelled() or task[1].done()):
                queries.append(task[1].get_name())
        return queries

    @staticmethod
    async def _remove_subscription(vdb_sub):
        try:
            task = SubscriptionManager._subscription_tasks[vdb_sub]
            if not task.cancelled():
                task.cancel()
                await task
        except asyncio.CancelledError:
            logger.info(
                "Unsubscribed from %s",
                task.get_name(),
            )
            return task
        except Exception as ex:
            logger.debug("Task status -> %s", task)
            logger.exception(ex)
            raise

    @staticmethod
    def _add_subscription(vdb_sub):
        try:
            task = asyncio.create_task(
                SubscriptionManager._subscribe_to_data_points_forever(vdb_sub),
                name=vdb_sub.query,
            )
            SubscriptionManager._subscription_tasks[vdb_sub] = task
            logger.info("Subscribing to %s", vdb_sub.query)
            return task
        except (grpc.aio.AioRpcError, Exception):  # type: ignore
            logger.exception("Error occured in SubscriptionManager._add_subscription.")
            raise

    # @retry((grpc.aio.AioRpcError), delay=2)
    @staticmethod
    async def _subscribe_to_data_points(vdb_sub):
        try:
            async for reply in vdb_sub.vdb_client.Subscribe(vdb_sub.query):
                reply_wrapper = DataPointReply(reply)
                if asyncio.iscoroutinefunction(vdb_sub.call_back):
                    await vdb_sub.call_back(reply_wrapper)
                else:
                    vdb_sub.call_back(reply_wrapper)
        except (grpc.aio.AioRpcError, Exception):  # type: ignore
            logger.exception(
                "Error occured in SubscriptionManager.subscribe_to_data_points."
            )
            raise

    @staticmethod
    async def _subscribe_to_data_points_forever(vdb_sub):
        while True:
            try:
                await SubscriptionManager._subscribe_to_data_points(vdb_sub)
            except (grpc.aio.AioRpcError, Exception) as ex:  # type: ignore
                logger.debug(
                    "Error in subscription -> {Subscription: %s}",
                    SubscriptionManager._subscription_tasks[vdb_sub],
                )
                logger.exception(ex)
                if isinstance(ex, (grpc.aio.AioRpcError)):  # type: ignore
                    if ex.code() is grpc.StatusCode.INVALID_ARGUMENT:
                        raise
                    logger.debug("Retrying after 2.5 seconds")
                    await asyncio.sleep(2.5)
                else:
                    raise


class VdbSubscription:
    """Expose subscription handling to client."""

    def __init__(self, vdb_client=None, query=None, call_back=None):
        self.query = query
        self.vdb_client = vdb_client
        self.call_back = call_back

    async def unsubscribe(self):
        try:
            task = await SubscriptionManager._remove_subscription(self)
            return task
        except Exception as ex:
            logger.exception(ex)

    async def subscribe(self):
        try:
            task = SubscriptionManager._subscription_tasks[self]
            if task.cancelled():
                SubscriptionManager._add_subscription(self)
            return task
        except Exception as ex:
            logger.exception(ex)
