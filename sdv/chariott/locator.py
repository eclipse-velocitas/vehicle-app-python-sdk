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
from sdv.locator import ServiceLocator
from sdv.proto.chariott.runtime.v1.runtime_pb2_grpc import ChariottService
from sdv.proto.chariott.runtime.v1.runtime_pb2 import FulfillRequest
from sdv.proto.chariott.common.v1.common_pb2 import DiscoverIntent, DiscoverFulfillment


class ChariottServiceLocator(ServiceLocator):
    """chariott based service locator"""

    async def get_location(self, service_name: str) -> str:
        fulfillRequest = FulfillRequest()
        fulfillRequest.namespace = f"sdv.{service_name.lower()}"
        fulfillRequest.intent = DiscoverIntent()
        service = ChariottService()
        result = await service.Fulfill(fulfillRequest)
        address = DiscoverFulfillment(result).services[0].url
        return address

    async def get_metadata(self, service_name: str):
        fulfillRequest = FulfillRequest()
        fulfillRequest.namespace = f"sdv.{service_name.lower()}"
        fulfillRequest.intent = DiscoverIntent()
        service = ChariottService()
        result = await service.Fulfill(fulfillRequest)
        app_id = DiscoverFulfillment(result).services[0].metadata.get("app-id")

        if app_id is None:
            app_id = service_name.lower()

        return (("app-id", str(app_id)),)