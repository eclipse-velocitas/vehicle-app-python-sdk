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

import asyncio
import logging
import signal

from sdv.vdb.subscriptions import DataPointReply
from sdv.vehicle_app import VehicleApp

from sdv_model import Vehicle, vehicle  # type: ignore

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.DEBUG)

"""Vehicle Data Broker Queries examples."""


async def on_speed_update(data: DataPointReply):
    logger.info(
        "Subscription: Vehicle.Speed: %f",
        data.get(vehicle.Speed).value,
    )


async def on_seat_pos_update(data: DataPointReply):
    logger.info(
        "Subscription: Vehicle.Speed: %f  Vehicle.Cabin.Seat.Row1.Pos1.Position: %i",
        data.get(vehicle.Speed).value,
        data.get(vehicle.Cabin.Seat.Row1.Pos1.Position).value,
    )


async def on_pos_condition_update(data: DataPointReply):
    logger.info(
        """Subscription: Vehicle.Speed: %f
        Warning: Vehicle.Cabin.Seat.Row1.Pos1.Position Exceeded 100""",
        data.get(vehicle.Speed).value,
    )


async def on_seat_speed_update(data: DataPointReply):
    logger.info(
        """Subscription: Vehicle.Speed: %f
        Warning: Vehicle.Cabin.Seat.Row1.Pos1.Position: %i is below 100""",
        data.get(vehicle.Speed).value,
        data.get(vehicle.Cabin.Seat.Row1.Pos1.Position).value,
    )


class VdbQueryExample(VehicleApp):
    """Speed Limit Warner Vehicle App"""

    def __init__(self, vehicle: Vehicle):
        super().__init__()
        self.Vehicle = vehicle

    async def on_start(self):
        """Run when the vehicle app starts"""
        pos = await self.Vehicle.Cabin.Seat.Row(1).Pos(1).Position.get()

        logger.info("Get: Vehicle.Cabin.Seat.Row1.Pos1.Position: %i", pos.value)

        vdb_rule = await self.Vehicle.Speed.where(
            "Vehicle.Cabin.Seat.Row1.Pos1.Position > 100"
        ).subscribe(on_pos_condition_update)

        await asyncio.sleep(10)
        await vdb_rule.unsubscribe()
        await asyncio.sleep(5)
        await vdb_rule.subscribe()

        await asyncio.sleep(5)
        await self.Vehicle.Speed.subscribe(on_speed_update)
        (
            await self.Vehicle.Cabin.Seat.Row(1)
            .Pos(1)
            .Position.join(self.Vehicle.Speed)
            .where("Vehicle.Cabin.Seat.Row1.Pos1.Position < 100")
            .subscribe(on_seat_speed_update)
        )
        (
            await self.Vehicle.Cabin.Seat.Row(1)
            .Pos(1)
            .Position.join(self.Vehicle.Speed)
            .subscribe(on_seat_pos_update)
        )


async def main():
    """Main function"""
    logging.basicConfig()
    print("Starting Vdb Query Sample...", flush=True)

    example = VdbQueryExample(vehicle)
    await example.run()


LOOP = asyncio.get_event_loop()
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop)
LOOP.run_until_complete(main())
LOOP.close()
