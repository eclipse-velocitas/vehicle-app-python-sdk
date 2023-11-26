# Copyright (c) 2022-2023 Contributors to the Eclipse Foundation
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

from velocitas_sdk.model import DataPointFloat, Model


class Vehicle(Model):
    """Sample Vehicle model."""

    def __init__(self):
        super().__init__()

        self.Speed = DataPointFloat("Speed", self)
        self.ThisIsAFloat = DataPointFloat("ThisIsAFloat", self)


class SubscribeException(Exception):
    """Custom Exception"""

    def __init__(self, datapoint) -> None:
        super().__init__()
        self.datapoint = datapoint


vehicle = Vehicle()
