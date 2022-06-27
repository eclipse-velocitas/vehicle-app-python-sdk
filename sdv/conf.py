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

from .dapr.locator import DaprServiceLocator

service_locator = DaprServiceLocator()

BROKER_APP_ID = os.getenv("VEHICLEDATABROKER_DAPR_APP_ID")
if BROKER_APP_ID is None:
    BROKER_APP_ID = "vehicledatabroker"
VEHICLE_DATA_BROKER_APP_ID = str(BROKER_APP_ID)

DAPR_PUB_SUB_NAME = "mqtt-pubsub"
DAPR_APP_PORT = 50008

VEHICLE_DATA_BROKER_ADDRESS: str = ""

DISABLE_DAPR = False
