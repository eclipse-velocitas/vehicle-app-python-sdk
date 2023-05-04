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

"""A sample app to set the Dogmode on the Vehicle."""
import os

os.environ["HVACSERVICE_DAPR_APP_ID"] = "hvacservice"

import asyncio
import json
import logging
import signal

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from vehicle_model.sample import Vehicle, vehicle

from sdv.util.log import get_default_date_format, get_default_log_format
from sdv.vdb.subscriptions import DataPointReply
from sdv.vehicle_app import VehicleApp, subscribe_data_points

logging.basicConfig(format=get_default_log_format(), datefmt=get_default_date_format())
logging.getLogger().setLevel("INFO")
logger = logging.getLogger(__name__)
TEMP_REPORT_TIMEOUT = 10


class DogModeApp(VehicleApp):
    """
    The Dog Mode Vehicle App.

    - receives DogModeOn message (MQTT or CAN) with the given temperature and
      activate A/C
    - set cabin temperature
    - publish the current cabin temperature every 10 sec

    if state of charge < 20 %
       sent MQTT message to notify owner
    """

    def __init__(self, vehicle: Vehicle):
        super().__init__()
        self.Vehicle = vehicle
        self.not_notified = True

    async def on_start(self):
        logger.info("VehicleApp Started ...")
        try:
            await self.display_values()
            self.scheduler = AsyncIOScheduler()
            self.scheduler.add_job(
                self.display_values, "interval", seconds=TEMP_REPORT_TIMEOUT
            )
            self.scheduler.start()
        except Exception as ex:
            logger.error(ex)

    async def on_pt_battery_stateofcharge(self, stateOfCharge):
        logger.info("Current Battery: %s", stateOfCharge)
        await self.publish_event("dogmode/stateOfCharge", json.dumps(stateOfCharge))

    @subscribe_data_points(
        """Vehicle.Cabin.DogModeTemperature, Vehicle.Cabin.DogMode,
        Vehicle.Powertrain.Battery.StateOfCharge.Current,
        Vehicle.Cabin.AmbientAirTemperature"""
    )
    async def on_change(self, data: DataPointReply):
        dogModeTemperature = data.get(self.Vehicle.Cabin.DogModeTemperature).value
        dogMode = data.get(self.Vehicle.Cabin.DogMode).value
        self.soc = data.get(self.Vehicle.Powertrain.Battery.StateOfCharge.Current).value
        self.temperature = data.get(self.Vehicle.Cabin.AmbientAirTemperature).value

        logger.info(
            "Current temperature of the desired Vehicle is: %s", self.temperature
        )

        await self.Vehicle.Cabin.HvacService.ToggleAcStatus(status=dogMode)
        if dogMode:
            await self.Vehicle.Cabin.HvacService.SetTemperature(
                temperature=dogModeTemperature
            )

        if self.soc < 20 and self.not_notified:
            self.not_notified = False
            await self.on_pt_battery_stateofcharge(self.soc)

        if self.soc < 10:
            await self.on_pt_battery_stateofcharge(self.soc)

        try:
            req_data = {"temperature": self.temperature}
            await self.publish_event(
                "dogmode/ambientAirTemperature", json.dumps(req_data)
            )
        except Exception as ex:
            logger.info(
                "Unable to get Current ambientAirTemperature, Exception: %s", ex
            )

    async def display_values(self):

        logger.info("Publish Current Temperature and StateOfCharge")
        try:
            logger.info(
                "Temperature and StateOfCharge are %s, %s", self.temperature, self.soc
            )
        except Exception as e:
            logger.info("Error getting the temperature %s", e)
            return

        json_data = {"Temperature": self.temperature, "StateOfCharge": self.soc}
        try:
            await self.publish_event("dogmode/display", json.dumps(json_data))
        except Exception as e:
            logger.info("An error occurred while trying to publish temperature %s", e)


async def main():
    """Main function"""
    logger.info("Starting dogmode app...")

    dogmode_app = DogModeApp(vehicle)
    await dogmode_app.run()


LOOP = asyncio.get_event_loop()
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop)
LOOP.run_until_complete(main())
LOOP.close()
