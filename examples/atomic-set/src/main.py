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

import asyncio
import json
import logging
import signal

from sdv_model import Vehicle, vehicle

from sdv.vdb.subscriptions import DataPointReply
from sdv.vehicle_app import VehicleApp, subscribe_topic

logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.DEBUG)

"""Vehicle Data Broker SetDatapoint examples."""

TOPIC_SET_VALUE_RESPONSE = "vehicleapp/setValue/response"
TOPIC_SET_VALUE_REQUEST = "vehicleapp/setValue/request"
# Payload:
# {"position": 300} -> this request for set seat position


class SetMultipleDatapointsAtomiclyApp(VehicleApp):
    """Speed Limit Warner Vehicle App"""

    def __init__(self, vehicle: Vehicle):
        super().__init__()
        self.vehicle = vehicle

    async def on_start(self):
        """Run when the vehicle app starts"""
        await vehicle.Cabin.Seat.Row1.Pos1.Position.subscribe(self.on_position_update)

    async def on_position_update(self, data: DataPointReply):
        logger.info(
            "Vehicle.Cabin.Seat.Row1.Pos1.Position: %i",
            data.get(vehicle.Cabin.Seat.Row1.Pos1.Position).value,
        )

    @subscribe_topic(TOPIC_SET_VALUE_REQUEST)
    async def on_set_actuator_recieved(self, data_str: str) -> None:
        data = json.loads(data_str)
        position = data["position"]
        logger.info("Set Position request %i", position)
        try:
            # This is a valid set request, the Position is an actuator.
            (await vehicle.preset(vehicle.Cabin.Seat.Row1.Pos1.Position, position)
                          .preset(vehicle.Cabin.Seat.Row1.Pos2.Position, position)
                          .apply())
            await self.publish_mqtt_event(
                TOPIC_SET_VALUE_RESPONSE, json.dumps(f".set({position}) request sent")
            )
        except TypeError as error:
            await self.publish_mqtt_event(
                TOPIC_SET_VALUE_RESPONSE, json.dumps(str(error))
            )


async def main():
    """Main function"""
    logging.basicConfig()
    logger.info("Starting SetDatapoint Sample...")

    example = SetMultipleDatapointsAtomiclyApp(vehicle)
    await example.run()


LOOP = asyncio.get_event_loop()
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop)
LOOP.run_until_complete(main())
LOOP.close()
