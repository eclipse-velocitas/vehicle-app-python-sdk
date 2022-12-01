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

from sdv.base import Middleware
from sdv.dapr.client import wait_for_sidecar
from sdv.dapr.server import run_server


class DaprMiddleware(Middleware):
    async def start(self):
        await run_server()

    async def wait_until_ready(self):
        await wait_for_sidecar()

    async def stop(self):
        pass
