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

from abc import ABC, abstractmethod


class AppConfig(ABC):
    """Velocitas App Config abstract base class."""

    def __init__(self) -> None:
        self.config = None

    def set_config(self, config: list[tuple()]):
        self.config = config

    # list of (key, value)
    @abstractmethod
    def get_config(self) -> list[tuple()]:
        raise NotImplementedError
