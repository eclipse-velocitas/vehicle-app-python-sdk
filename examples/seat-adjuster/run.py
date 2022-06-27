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

"""Seat Adjuster example."""

import asyncio
import json
import logging
import signal

from sdv_model import Vehicle, vehicle
from set_position_request_processor import SetPositionRequestProcessor

from sdv import conf
from sdv.dapr.locator import DaprServiceLocator
from sdv.util.log import get_default_date_format, get_default_log_format
from sdv.vehicle_app import VehicleApp, subscribe_data_points, subscribe_topic

logging.basicConfig(format=get_default_log_format(), datefmt=get_default_date_format())
logging.getLogger().setLevel("INFO")
logger = logging.getLogger(__name__)


class SeatAdjuster(VehicleApp):
    """Seat adjuster Vehicle App"""

    def __init__(self, vehicle_client: Vehicle):
        super().__init__()
        self.vehicle_client = vehicle_client
        self.vehicle_speed = 0

    @subscribe_topic("seatadjuster/setPosition/request")
    async def on_set_position_request_received(self, data: str) -> None:
        """Handle set position request from GUI app from MQTT topic"""
        data = json.loads(data)
        logger.info("Set Position Request received: data=%s", data)  # noqa: E501
        await self._on_set_position_request_received(
            data, "seatadjuster/setPosition/response"
        )

    async def _on_set_position_request_received(
        self, data: str, resp_topic: str
    ) -> None:
        vehicle_speed = self.vehicle_speed
        logger.info("Current Speed is: %s", vehicle_speed)
        if vehicle_speed == 0:
            logger.info("Vehicle is not moving, proceeding ...")
            processor = SetPositionRequestProcessor(self.vehicle_client)
            await processor.process(data, resp_topic, self)
        else:
            logger.warning(
                "Not allowed to move seat because vehicle speed is %s and not 0",
                vehicle_speed=vehicle_speed,
            )

    @subscribe_data_points("Vehicle.Cabin.Seat.Row1.Pos1.Position, Vehicle.Speed")
    async def on_seat_position_change(self, data):
        """Handle seat position change change"""
        self.vehicle_speed = data.fields["Vehicle.Speed"].float_value
        logger.info("Current Vehicle Speed is: %s", self.vehicle_speed)

        resp_data = data.fields["Vehicle.Cabin.Seat.Row1.Pos1.Position"].uint32_value
        req_data = {"position": resp_data}
        logger.info("Current Position of the Vehicle Seat is: %s", req_data)
        try:
            await self.publish_mqtt_event(
                "seatadjuster/currentPosition", json.dumps(req_data)
            )
        except Exception as ex:
            logger.info("Unable to get Current Seat Position, Exception: %s", ex)
            resp_data = {"requestId": data["requestId"], "status": 1, "message": ex}
            await self.publish_mqtt_event(
                "seatadjuster/currentPosition", json.dumps(resp_data)
            )


async def main():
    """Main function"""
    logging.basicConfig()
    print("Starting seat adjuster app...", flush=True)
    conf.service_locator = DaprServiceLocator()
    seat_adjuster = SeatAdjuster(vehicle)
    await seat_adjuster.run()


LOOP = asyncio.get_event_loop()
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop)
LOOP.run_until_complete(main())
LOOP.close()
