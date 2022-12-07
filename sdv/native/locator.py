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
import os
from typing import Optional

from sdv.base import ServiceLocator

logger = logging.getLogger(__name__)

APP_PORT_ID = "dapr-app-port"
APP_PORT = "50008"


class NativeServiceLocator(ServiceLocator):
    """Middleware descriptor abstract base class."""

    def __init__(self) -> None:
        self.default_addresses = {
            "mqtt": "mqtt://localhost:1883",
            "vehicledatabroker": "grpc://localhost:55555",
        }

    def get_service_location(self, service_name: str) -> str:
        address = os.getenv("SDV_" + service_name.upper() + "_ADDRESS")
        if address is None:
            try:
                address = self.default_addresses[service_name.lower()]
            except KeyError:
                logger.error(
                    """Can't find the service location for %s, make sure to set the
                    necessary env variables for all depemdencies""",
                    service_name,
                )

        return str(address)

    def get_metadata(self, service_name: Optional[str] = None):
        if service_name is None:
            service_name = ""

        return ((APP_PORT_ID, APP_PORT),)
