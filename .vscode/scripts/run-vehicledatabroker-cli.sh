#!/bin/bash
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

echo "#######################################################"
echo "### Running VehicleDataBroke CLI                    ###"
echo "#######################################################"

ROOT_DIRECTORY=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/../.." )
source $ROOT_DIRECTORY/.vscode/scripts/exec-check.sh "$@" $(basename $BASH_SOURCE .sh)
DATABROKER_VERSION=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .databroker.version | tr -d '"')

sudo chown $(whoami) $HOME
DATABROKER_ASSET_FOLDER="$ROOT_DIRECTORY/.vscode/scripts/assets/databroker/$DATABROKER_VERSION"
DOWNLOAD_URL=https://github.com/boschglobal/kuksa.val/releases/download

#Detect host environment (distinguish for Mac M1 processor)
if [[ `uname -m` == 'aarch64' || `uname -m` == 'arm64' ]]; then
    echo "Detected ARM architecture"
    PROCESSOR="aarch64"
    DATABROKER_BINARY_NAME="databroker_aarch64.tar.gz"
    DATABROKER_EXEC_PATH="$DATABROKER_ASSET_FOLDER/$PROCESSOR/target/aarch64-unknown-linux-gnu/release"
else
    echo "Detected x86_64 architecture"
    PROCESSOR="x86_64"
    DATABROKER_BINARY_NAME='databroker_x86_64.tar.gz'
    DATABROKER_EXEC_PATH="$DATABROKER_ASSET_FOLDER/$PROCESSOR/target/release"
fi

if [[ ! -f "$DATABROKER_EXEC_PATH/databroker" ]]
then
  echo "Downloading databroker:$DATABROKER_VERSION"
  curl -o $DATABROKER_ASSET_FOLDER/$PROCESSOR/$DATABROKER_BINARY_NAME --create-dirs -L -H "Accept: application/octet-stream" "$DOWNLOAD_URL/$DATABROKER_VERSION/$DATABROKER_BINARY_NAME"
  tar -xf $DATABROKER_ASSET_FOLDER/$PROCESSOR/$DATABROKER_BINARY_NAME -C $DATABROKER_ASSET_FOLDER/$PROCESSOR
fi

$DATABROKER_EXEC_PATH/databroker-cli
