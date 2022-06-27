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

"""This module contains the SetPositionRequestProcessor class."""

import json
import logging
import traceback

from sdv_model import Vehicle
from sdv_model.proto.seats_pb2 import BASE, SeatLocation

from sdv.vehicle_app import VehicleApp

logger = logging.getLogger(__name__)


class SetPositionRequestProcessor:
    """A class to process position requests."""

    def __init__(self, vehicle_client: Vehicle) -> None:
        self.vehicle_client = vehicle_client

    async def process(
        self,
        data: str,
        resp_topic: str,
        app: VehicleApp,
    ):
        """Process the position request."""
        resp_data = await self.__get_processed_response(data)
        await self.__publish_data_to_topic(resp_data, resp_topic, app)

    async def __get_processed_response(self, data):
        try:
            location = SeatLocation(row=1, index=1)
            logger.info(
                "Sending command to seat service to move seat %s", data["position"]
            )
            await self.vehicle_client.Cabin.SeatService.MoveComponent(
                location, BASE, data["position"]  # type: ignore
            )
            resp_data = {"requestId": data["requestId"], "result": {"status": 0}}
        except Exception as ex:
            logger.error(traceback.format_exc())
            resp_data = {
                "requestId": data["requestId"],
                "result": {"status": 1, "message": self.__get_error_message_from(ex)},
            }
        return resp_data

    async def __publish_data_to_topic(
        self, resp_data: dict, resp_topic: str, app: VehicleApp
    ):
        status = 0
        try:
            await app.publish_mqtt_event(resp_topic, json.dumps(resp_data))
        except Exception:
            status = -1
        return status

    def __get_error_message_from(self, ex: Exception):
        return "Exception details: " + ex.args[0].debug_error_string
