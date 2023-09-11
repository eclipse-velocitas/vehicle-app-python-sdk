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
from typing import Optional

from velocitas_sdk.base import ServiceLocator

DAPR_APP_ID_KEY = "dapr-app-id"
DAPR_APP_PORT_KEY = "dapr-app-port"
DAPR_APP_PORT_VALUE = 50008

DAPR_PUB_SUB_NAME_VALUE = "mqtt-pubsub"


class DaprServiceLocator(ServiceLocator):
    """Middleware descriptor abstract base class."""

    def get_service_location(self, service_name: str) -> str:
        env_var = os.getenv("DAPR_GRPC_PORT")
        if env_var is None:
            port = 51001
        else:
            port = int(str(os.getenv("DAPR_GRPC_PORT")))

        address = f"grpc://localhost:{port}"
        return address

    def get_metadata(self, service_name: Optional[str] = None):
        if service_name is None:
            service_name = ""

        app_id = os.getenv(service_name.upper() + "_DAPR_APP_ID")
        if app_id is None:
            app_id = service_name.lower()

        return ((DAPR_APP_ID_KEY, str(app_id)),)
