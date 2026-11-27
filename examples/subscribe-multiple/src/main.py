# Copyright (c) 2022-2026 Contributors to the Eclipse Foundation
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

"""Speed Warner example."""

import asyncio
import logging
import signal

from vehicle import Vehicle, vehicle  # type: ignore

from velocitas_sdk.vdb.subscriptions import DataPointReply
from velocitas_sdk.vehicle_app import VehicleApp

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.DEBUG)


class VehicleLocationTracker(VehicleApp):
    """Speed Limit Warner Vehicle App"""

    def __init__(self, vehicle: Vehicle):
        super().__init__()
        self.Vehicle = vehicle

    async def on_start(self):
        """Run when the vehicle app starts"""

        await (
            self.Vehicle.CurrentLocation.Latitude.join(
                self.Vehicle.CurrentLocation.Longitude
            )
            .join(self.Vehicle.Speed)
            .subscribe(self.on_location_update)
        )

    def on_location_update(self, data: DataPointReply):
        """Handle vehicle speed limit exceeded event"""
        logger.info(
            "Vehicle location updated: (%f, %f) at %f km/h",
            data.get(self.Vehicle.CurrentLocation.Latitude).value,
            data.get(self.Vehicle.CurrentLocation.Longitude).value,
            data.get(self.Vehicle.Speed).value,
        )


async def main():
    """Main function"""
    logging.basicConfig()
    print("Starting speed limit warner...", flush=True)
    warner = VehicleLocationTracker(vehicle)
    await warner.run()


LOOP = asyncio.get_event_loop()
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop)
LOOP.run_until_complete(main())
LOOP.close()
