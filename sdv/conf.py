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

from sdv.chariott.locator import ChariottServiceLocator
from sdv.dapr.locator import DaprServiceLocator
from sdv.locator import NativeGrpcServiceLocator

DAPR_PUB_SUB_NAME = "mqtt-pubsub"
DAPR_APP_PORT = 50008
DISABLE_DAPR = os.getenv("VELOCITAS_DISABLE_DAPR", True)
middleware_type = os.getenv("VELOCITAS_MIDDLEWARE_TYPE", "chariot")
service_locator = NativeGrpcServiceLocator()
if middleware_type == "dapr":
    service_locator = DaprServiceLocator()
elif middleware_type == "chariot":
    service_locator = ChariottServiceLocator()
