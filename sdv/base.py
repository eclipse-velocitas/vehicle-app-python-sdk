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


from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class MiddlewareType(str, Enum):
    """Enumerator for the supported Velocitas Middlewares."""

    NATIVE = "native"
    DAPR = "dapr"


class ServiceLocator(ABC):
    """Service Discovery Locator abstract base class."""

    @abstractmethod
    def get_service_location(self, service_name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self, service_name: Optional[str] = None):
        raise NotImplementedError


class PubSubClient(ABC):
    """PubSub client descriptor abstract base class."""

    @abstractmethod
    async def init(self):
        raise NotImplementedError

    @abstractmethod
    async def run(self):
        raise NotImplementedError

    @abstractmethod
    async def register_topic(self, topic: str, coro):
        raise NotImplementedError

    @abstractmethod
    async def publish_event(self, topic: str, data: str):
        raise NotImplementedError
