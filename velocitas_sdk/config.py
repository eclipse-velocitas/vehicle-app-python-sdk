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

import os

from velocitas_sdk.base import Middleware, MiddlewareType
from velocitas_sdk.dapr.middleware import DaprMiddleware
from velocitas_sdk.native.middleware import NativeMiddleware


class Config:
    """General configuration of the vehicle app"""

    def __init__(self, *args):
        if len(args) > 1:
            raise ValueError("Only one middleware type is supported at a time!")

        if isinstance(args[0], str):
            __middleware = MiddlewareType(args[0])
        elif isinstance(args[0], MiddlewareType):
            __middleware = args[0]
        else:
            raise ValueError(f"Not supported middleware type {args[0]}")

        self.middleware: Middleware = self.__create_middleware(__middleware)

    def __create_middleware(self, middleware_type: str) -> Middleware:
        _middleware: Middleware
        if middleware_type == MiddlewareType.NATIVE.value:
            _middleware = NativeMiddleware()
        if middleware_type == MiddlewareType.DAPR.value:
            _middleware = DaprMiddleware()

        return _middleware


__middleware_type = os.getenv("SDV_MIDDLEWARE_TYPE", MiddlewareType.DAPR.value)
_config = Config(__middleware_type)

middleware = _config.middleware
