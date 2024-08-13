# Copyright (c) 2022-2024 Contributors to the Eclipse Foundation
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

import sys
from urllib.parse import urlparse

from velocitas_sdk.base import Middleware, MiddlewareType
from velocitas_sdk.native.locator import NativeServiceLocator
from velocitas_sdk.native.mqtt import MqttClient


class NativeMiddleware(Middleware):
    """Native middleware implementation."""

    def __init__(self) -> None:
        super().__init__()

        self.type = MiddlewareType.NATIVE
        self.service_locator = NativeServiceLocator()

        _address = self.service_locator.get_service_location("mqtt")
        _port = urlparse(_address).port
        _hostname = urlparse(_address).hostname

        if _hostname is None:
            print("No hostname")
            sys.exit(-1)

        self.pubsub_client = MqttClient(hostname=_hostname, port=_port)

    async def start(self):
        await self.pubsub_client.init()

    async def wait_until_ready(self):
        pass

    async def stop(self):
        pass
