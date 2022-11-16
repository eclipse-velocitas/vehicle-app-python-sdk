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
from typing import Optional
from typing import Iterator
import grpc 
import sdv.conf as conf
from sdv.proto.chariott.common.v1.common_pb2 import (
    WriteIntent,
    SubscribeIntent,
    Intent,
    Value
)
from sdv.proto.chariott.runtime.v1.runtime_pb2_grpc import ChariottServiceStub
from sdv.proto.chariott.runtime.v1.runtime_pb2 import FulfillRequest
from sdv.proto.chariott.streaming.v1.streaming_pb2 import OpenRequest, Event
from sdv.proto.chariott.streaming.v1.streaming_pb2_grpc import ChannelServiceStub


class ChariottPubSubClient:
    """This class is a wrapper for the on_message callback of the chariott KV store"""

    def __init__(self, port: Optional[int] = None, hostname: Optional[str] = None):
        self._subscriptions = []
        self._kv_namespace = "sdv.kvs"
        self._service_address = conf.service_locator.get_location(self._kv_namespace)
        self._registered_topics = []
        self._topics_waiting_for_subscription = []
        self._initialized = False
        self._channel_id = ""

    def __on_connect(self):
        self.__register_waiting_topics()

    async def run(self):
        """Do nothing"""

    async def _message_watcher(
            self,
            message_iterator: Iterator[Event]) -> None:
        try:
            for message in message_iterator:
                print(message)
§         except Exception as e:
            print(e)
            raise

    async def init(self):
        with grpc.insecure_channel(self._service_address) as channel:
            service_stub = ChannelServiceStub(channel)
            stream = service_stub.Open(OpenRequest())
            self._channel_id = dict(stream.initial_metadata())["x-chariott-channel-id"]

            task = asyncio.create_task(
                coro=self._message_watcher(stream),
                name='sdv.kvs'
            )
            self._subscriptions.append(task)

            self._initialized = True
            self.__on_connect()
            

    def __register_waiting_topics(self):
        if not self._initialized: 
            return
        for topic in self._topics_waiting_for_subscription:
            self.__register_topic(topic["topic"], topic["coro"])

    def __register_topic(self, topic, coro):
        self._registered_topics.append({
            "topic": topic,
            "coro": coro
        })

        fulfill_request = FulfillRequest(
            namespace=self._kv_namespace,
            intent=Intent(subscribe=SubscribeIntent(
                channel_id=self._channel_id, 
                sources=[topic])
            ),
        )

        with grpc.insecure_channel("localhost:4243") as channel:
            service_stub = ChariottServiceStub(channel)
            service_stub.Fulfill(fulfill_request)

    def register_topic(self, topic, coro):
        self._topics_waiting_for_subscription.append(
            {"topic": topic, "coro": coro}
        )

        self.__register_waiting_topics()

    def publish_event(self, topic: str, data: str) -> None:
        fulfill_request = FulfillRequest(
            namespace=self._kv_namespace,
            intent=Intent(write=WriteIntent(key=topic, value=Value(string=data))),
        )

        with grpc.insecure_channel("localhost:4243") as channel:
            service_stub = ChariottServiceStub(channel)
            service_stub.Fulfill(fulfill_request)
