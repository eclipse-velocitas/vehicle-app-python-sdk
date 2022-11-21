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

"""" dapr gateway"""

from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import grpc
from dapr.proto import appcallback_service_v1  # type: ignore

from sdv.dapr._servicier import TopicSubscribeCallable, _CallbackServicer
from sdv.dapr.locator import DaprServiceLocator

_service_locator = DaprServiceLocator()


class _DaprServer:
    def __init__(self):
        self._port = _service_locator.get_metadata("")[0][1]
        self._worker_thread = Thread(target=self._start_server_loop)
        self._worker_thread.daemon = True
        self._is_running = False

    def start(self):
        """Starts the server."""
        if self._is_running is False:
            self._worker_thread.start()
            self._is_running = True

    def _start_server_loop(self):
        server = grpc.server(ThreadPoolExecutor(max_workers=10))
        appcallback_service_v1.add_AppCallbackServicer_to_server(_servicer, server)
        server.add_insecure_port(f"[::]:{self._port}")
        server.start()
        server.wait_for_termination()


_dapr_server = _DaprServer()


async def run_server():
    _dapr_server.start()


_servicer = _CallbackServicer()


def register_topic(topic: str, callback: TopicSubscribeCallable) -> None:
    """Register a callback method as a MQTT topic subscriber over dapr pub/sub.

    Args:
        topic (str): MQTT topic name
        callback (TopicSubscribeCallable): method to be be called on incoming messages
    """
    pubsub_name = _service_locator.get_metadata("pubsub")
    _servicer.register_topic(
        pubsub_name[0][1], topic, callback, metadata={"rawPayload": "true"}
    )
