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

from sdv.locator import ServiceLocator

DAPR_PUB_SUB_NAME = "mqtt-pubsub"


class DaprServiceLocator(ServiceLocator):
    """dapr service locator"""

    def get_location(self, service_name: str) -> str:
        env_var = os.getenv("DAPR_GRPC_PORT")
        if env_var is None:
            port = 51001
        else:
            port = int(str(os.getenv("DAPR_GRPC_PORT")))

        address = f"localhost:{port}"
        return address

    def get_metadata(self, service_name: str):
        if service_name == "pubsub":
            return (("name", DAPR_PUB_SUB_NAME),)

        app_id = os.getenv(service_name.upper() + "_DAPR_APP_ID")
        if app_id is None:
            app_id = service_name.lower()

        return (("dapr-app-id", str(app_id)),)
