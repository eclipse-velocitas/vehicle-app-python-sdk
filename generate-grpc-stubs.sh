#!/bin/zsh
# Copyright (c) 2023 Robert Bosch GmbH and Microsoft Corporation
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

echo "#######################################################"
echo "### Generating gRPC stubs from proto files          ###"
echo "#######################################################"

set -x

ROOT_DIR=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" )
python3 -m grpc_tools.protoc -I ./velocitas_sdk/proto --grpc_python_out=./velocitas_sdk/proto --python_out=./velocitas_sdk/proto --mypy_out=./velocitas_sdk/proto ./velocitas_sdk/proto/**/*.proto
mv -f ./velocitas_sdk/proto/**/*.py ./velocitas_sdk/proto
mv -f ./velocitas_sdk/proto/**/*.pyi ./velocitas_sdk/proto

sed -i -e 's/from sdv\..* import/from velocitas_sdk.proto import/g' -e 's/import sdv\..*\./import velocitas_sdk.proto./g' ./velocitas_sdk/proto/*.py*
