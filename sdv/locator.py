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
from abc import ABC, abstractmethod


class ServiceLocator(ABC):
    """Service Locator abstract base class."""
    def __init__(self) -> None:
        self._services: list[tuple[str, str]] = [] 

    @abstractmethod
    def get_metadata(self, service_name: str):
        raise NotImplementedError

    def add_service(self, service_name: str, address: str):
        self._services.append((service_name, address))

    def get_location(self, service_name: str):
        address = None
        for service in self._services:
            if (service[0] != service_name):
                continue
            address = service[1]
            break

        return address


class NativeGrpcServiceLocator(ServiceLocator):
    """native grpc service locator"""

    def get_location(self, service_name: str) -> str:
        address = os.getenv("SDV_" + service_name.upper() + "_ADDRESS", None)
        if address is None:
            address = super.get_location(service_name)
        return address

    def get_metadata(self, service_name: str):
        app_id = os.getenv("SDV_" + service_name.upper() + "_ID")
        if app_id is None:
            app_id = service_name.lower()

        return (("app-id", str(app_id)),)
