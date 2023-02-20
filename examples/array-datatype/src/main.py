# Copyright (c) 2022-2023 Robert Bosch GmbH and Microsoft Corporation
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

"""Array Datatype example."""

import asyncio
import logging
import signal

from vehicle_model.sample import Vehicle, vehicle

from sdv.vdb.subscriptions import DataPointReply
from sdv.vehicle_app import VehicleApp

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.DEBUG)


class ArrayDatatype(VehicleApp):
    """Array Datatype example Vehicle App"""

    def __init__(self, vehicle: Vehicle):
        super().__init__()
        self.vehicle = vehicle

    def print_values(self, data: DataPointReply):
        """Handle string array limit exceeded event"""

        logger.info(
            "Example Array contains: %s", data.get(self.vehicle.TestArray).value
        )

    async def on_start(self):
        """Run when the vehicle app starts"""

        await self.vehicle.TestArray.subscribe(self.print_values)


async def main():
    """Main function"""
    logging.basicConfig()
    print("Starting Array Datatype example...", flush=True)

    array = ArrayDatatype(vehicle)
    await array.run()


LOOP = asyncio.get_event_loop()
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop)
LOOP.run_until_complete(main())
LOOP.close()
