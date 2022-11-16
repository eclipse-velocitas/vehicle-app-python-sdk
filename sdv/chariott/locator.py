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
import grpc

from sdv.locator import ServiceLocator
from sdv.proto.chariott.common.v1.common_pb2 import (
    DiscoverFulfillment,
    DiscoverIntent,
    Intent,
)
from sdv.proto.chariott.runtime.v1.runtime_pb2 import FulfillRequest
from sdv.proto.chariott.runtime.v1.runtime_pb2_grpc import ChariottServiceStub


class ChariottServiceLocator(ServiceLocator):
    """chariott based service locator"""

    def get_location(self, service_name: str) -> str:
        fulfill_request = FulfillRequest(
            namespace=f"{service_name.lower()}",
            intent=Intent(discover=DiscoverIntent()),
        )

        with grpc.insecure_channel("localhost:4243") as channel:
            service_stub = ChariottServiceStub(channel)
            result = service_stub.Fulfill(fulfill_request)
            address = result.fulfillment.discover.services[0].url \
                .replace("http://", "") \
                .replace("/", "")
            return address

    def get_metadata(self, service_name: str):
        return service_name.lower()