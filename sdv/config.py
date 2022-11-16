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

from enum import Enum

from sdv.dapr.locator import DaprServiceLocator
from sdv.locator import NativeGrpcServiceLocator, ServiceLocator


class Middleware(str, Enum):
    """Enumerator for the supported Velocitas Middlewares."""

    NATIVE = "native"
    DAPR = "dapr"


class Config:
    """General configuration of the vehicle app"""

    def __init__(self, *args):
        if len(args) > 1:
            raise ValueError("........")
        elif isinstance(args[0], str):
            self.middleware_value = args[0]
        elif isinstance(args[0], Middleware):
            # This will raise a KeyError is the middleware is not supported.
            self.middleware_value = Middleware._value2member_map_[args[0]]

        self.service_locator = self.__create_locator(self.middleware_value)

    def __create_locator(self, middleware: str) -> ServiceLocator:
        if middleware == Middleware.NATIVE.value:
            return NativeGrpcServiceLocator()
        if middleware == Middleware.DAPR.value:
            return DaprServiceLocator()

    @classmethod
    def dump(cls):
        print(f"Middleware: {cls.middleware}, ServiceLocator: {cls.service_locator}")
