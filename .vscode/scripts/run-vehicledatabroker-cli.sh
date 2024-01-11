#!/bin/bash
# Copyright (c) 2022-2024 Contributors to the Eclipse Foundation
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
echo "### Running VehicleDataBroker CLI                   ###"
echo "#######################################################"

ROOT_DIRECTORY=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/../.." )
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source $ROOT_DIRECTORY/.vscode/scripts/exec-check.sh "$@" $(basename $BASH_SOURCE .sh)
DATABROKER_VERSION=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .databroker.version | tr -d '"')

sudo chown $(whoami) $HOME
# Needed because of how the databroker release is tagged
DATABROKER_ASSET_FOLDER="$SCRIPT_DIR/assets/databroker/$DATABROKER_VERSION"
#Detect host environment (distinguish for Mac M1 processor)
if [[ `uname -m` == 'aarch64' || `uname -m` == 'arm64' ]]; then
    echo "Detected ARM architecture"
    PROCESSOR="aarch64"
    DATABROKER_BINARY_NAME="databroker-cli-arm64.tar.gz"
else
    echo "Detected x86_64 architecture"
    PROCESSOR="x86_64"
    DATABROKER_BINARY_NAME='databroker-cli-amd64.tar.gz'
fi

DATABROKER_EXEC_PATH="$DATABROKER_ASSET_FOLDER/$PROCESSOR/databroker-cli"

if [[ ! -f "$DATABROKER_EXEC_PATH/databroker-cli" ]]
then
    DOWNLOAD_URL=https://github.com/eclipse/kuksa.val/releases/download
    echo "Downloading databroker:$DATABROKER_VERSION"
    curl -o $DATABROKER_ASSET_FOLDER/$PROCESSOR/$DATABROKER_BINARY_NAME --create-dirs -L -H "Accept: application/octet-stream" "$DOWNLOAD_URL/$DATABROKER_VERSION/$DATABROKER_BINARY_NAME"
    tar -xf $DATABROKER_ASSET_FOLDER/$PROCESSOR/$DATABROKER_BINARY_NAME -C $DATABROKER_ASSET_FOLDER/$PROCESSOR
fi

$DATABROKER_EXEC_PATH/databroker-cli
