# Copyright (c) 2023 Contributors to the Eclipse Foundation
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
import sys

# Get the app directory path
app_dir_path = os.path.abspath(os.path.join(__file__, "../../.."))

# Add the src directory to the sys.path
src_dir = os.path.join(app_dir_path, "src")
sys.path.insert(0, src_dir)

# Import the AppName class from vapp.py
from vapp import AppName  # type: ignore # noqa: E402


async def test_instantiation():
    my_app = AppName()

    assert my_app is not None
    print("MyApp instantiated!")
