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


"""Sample Vehicle Data Model"""

from vehicle_model.proto.hvac_pb2 import (
    AcStatus,
    SetAcStatusRequest,
    SetTemperatureRequest,
)
from vehicle_model.proto.hvac_pb2_grpc import HvacStub

from sdv.model import DataPointBoolean, DataPointFloat, Model, Service


class HvacService(Service):
    "HVAC Service model"

    def __init__(self):
        super().__init__()
        self._stub = HvacStub(self.channel)

    async def ToggleAcStatus(self, status: bool):
        if status:
            response = await self._stub.SetAcStatus(
                SetAcStatusRequest(status=AcStatus.ON), metadata=self.metadata
            )
        else:
            response = await self._stub.SetAcStatus(
                SetAcStatusRequest(status=AcStatus.OFF), metadata=self.metadata
            )
        return response

    async def SetTemperature(
        self,
        temperature: float,
    ):
        response = await self._stub.SetTemperature(
            SetTemperatureRequest(
                temperature=temperature,  # type: ignore
            ),
            metadata=self.metadata,
        )
        return response


class Cabin(Model):
    "Cabin model."

    def __init__(self, parent):
        super().__init__(parent)

        # Dogmode Sample
        self.HvacService = HvacService()
        self.IsAirConditioningActive = DataPointBoolean("IsAirConditioningActive", self)
        self.DogMode = DataPointBoolean("DogMode", self)
        self.AmbientAirTemperature = DataPointFloat("AmbientAirTemperature", self)
        self.DesiredAmbientAirTemperature = DataPointFloat(
            "DesiredAmbientAirTemperature", self
        )
        self.DogModeTemperature = DataPointFloat("DogModeTemperature", self)


class Battery(Model):
    """Battery model"""

    def __init__(self, parent: Model):
        super().__init__(parent)
        self.StateOfCharge = StateOfCharge(self)


class Powertrain(Model):
    """Powertrain model"""

    def __init__(self, parent: Model):
        super().__init__(parent)
        self.Battery = Battery(self)


class StateOfCharge(Model):
    """StateOfCharge model"""

    def __init__(self, parent: Model):
        super().__init__(parent)
        self.Current = DataPointFloat("Current", self)


class Vehicle(Model):
    """Sample Vehicle model."""

    def __init__(self):
        super().__init__()

        self.Powertrain = Powertrain(self)
        self.Speed = DataPointFloat("Speed", self)
        self.Cabin = Cabin(self)


vehicle = Vehicle()
