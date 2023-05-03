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

"""Speed Warner example."""

import argparse
import asyncio
import json
import logging
import signal

from sdv_model import Vehicle, vehicle  # type: ignore

from sdv import config
from sdv.config import Config, MiddlewareType
from sdv.vdb.subscriptions import DataPointReply
from sdv.vehicle_app import VehicleApp, subscribe_topic

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.DEBUG)


class SpeedLimitWarner(VehicleApp):
    """Speed Limit Warner Vehicle App"""

    def __init__(self, vehicle: Vehicle, speed_limit: float):
        super().__init__()
        self.Vehicle = vehicle
        self.speed_limit = speed_limit

    @subscribe_topic("speedlimitwarner/setLimit/request")
    async def on_change_speed_limit_request(self, data: str) -> None:
        """Handle change speed limit request from GUI app from MQTT topic"""
        data = json.loads(data)
        logger.info("Change speed limit received: data=%s", data)  # noqa: E501
        self.speed_limit = data["speed"]
        condition = f"Vehicle.Speed > {self.speed_limit}"

        await self.rule.unsubscribe()
        self.rule = (
            await self.Vehicle.Speed.join(self.Vehicle.ADAS.ABS.IsEngaged)
            .where(condition)
            .subscribe(self.on_vehicle_speed_above_limit)
        )

    def on_vehicle_speed_above_limit(self, data: DataPointReply):
        """Handle vehicle speed limit exceeded event"""
        logger.info(
            "Warning: Vehicle speed limit (%s) exceeded: %f. ABS is engaged: %s",
            self.speed_limit,
            data.get(self.Vehicle.Speed).value,
            data.get(self.Vehicle.ADAS.ABS.IsEnabled).value,
        )

    async def on_start(self):
        """Run when the vehicle app starts"""

        condition = f"Vehicle.Speed > {self.speed_limit}"
        self.rule = (
            await self.Vehicle.Speed.join(self.Vehicle.ADAS.ABS.IsEngaged)
            .where(condition)
            .subscribe(self.on_vehicle_speed_above_limit)
        )


async def main():
    """Main function"""
    logging.basicConfig()
    args = parser.parse_args()
    if not args.enable_dapr:
        logger.debug("Init native middleware")
        config._config = Config(MiddlewareType.NATIVE)
    else:
        logger.debug("Init dapr middleware")
        config._config = Config(MiddlewareType.DAPR)

    print("Starting speed limit warner...", flush=True)

    warner = SpeedLimitWarner(vehicle, args.limit)
    await warner.run()


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--limit", help="Speed limit", default=130.0)
parser.add_argument("-e", "--enable-dapr", help="Enable dapr", action="store_true")

LOOP = asyncio.get_event_loop()
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop)
LOOP.run_until_complete(main())
LOOP.close()
