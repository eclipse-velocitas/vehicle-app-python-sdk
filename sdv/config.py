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

import os

from sdv.base import MiddlewareType, PubSubClient, ServiceLocator
from sdv.dapr.locator import DaprServiceLocator
from sdv.dapr.pubsub import DaprClient
from sdv.native.locator import NativeServiceLocator
from sdv.native.mqtt import MqttClient


class Config:
    """General configuration of the vehicle app"""

    def __init__(self, *args):
        if len(args) > 1:
            raise ValueError("Only one middleware type is supported at a time!")
        elif isinstance(args[0], str):
            __middleware = MiddlewareType(args[0])
        elif isinstance(args[0], MiddlewareType):
            __middleware = args[0]
        else:
            raise ValueError(f"Not supported middleware type {args[0]}")

        self.middleware_type: MiddlewareType = __middleware
        self.service_locator = self.__service_locator(self.middleware_type.value)
        self.pubsub_client = self.__pubsub_client(self.middleware_type.value)

    def __service_locator(self, middleware_type: str) -> ServiceLocator:
        if middleware_type == MiddlewareType.NATIVE.value:
            locateor: ServiceLocator = NativeServiceLocator()
        if middleware_type == MiddlewareType.DAPR.value:
            locateor: ServiceLocator = DaprServiceLocator()

        return locateor

    def __pubsub_client(self, middleware_type: str) -> PubSubClient:
        if middleware_type == MiddlewareType.NATIVE.value:
            client: PubSubClient = MqttClient()
        if middleware_type == MiddlewareType.DAPR.value:
            client: PubSubClient = DaprClient()

        return client

    @classmethod
    def dump(cls):
        print(
            f"Middleware: {cls.middleware_type}, ServiceLocator: {cls.service_locator}"
        )


DISABLE_DAPR: bool = True
__middleware_type = os.getenv("SDV_MIDDLEWARE_TYPE", MiddlewareType.DAPR.value)
__config = Config(__middleware_type)

middleware_type = __config.middleware_type
service_locator = __config.service_locator
pubsub_client = __config.pubsub_client
