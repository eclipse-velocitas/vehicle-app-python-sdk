#!/bin/bash
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
echo "### Running Seatservice                             ###"
echo "#######################################################"

ROOT_DIRECTORY=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/../.." )
source $ROOT_DIRECTORY/.vscode/scripts/exec-check.sh "$@" $(basename $BASH_SOURCE .sh)

SEATSERVICE_VERSION=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .seatservice.version | tr -d '"')
SEATSERVICE_PORT='50051'
SEATSERVICE_GRPC_PORT='52002'
sudo chown $(whoami) $HOME

SEATSERVICE_ASSET_FOLDER="$ROOT_DIRECTORY/.vscode/scripts/assets/seatservice/$SEATSERVICE_VERSION"
#Detect host environment (distinguish for Mac M1 processor)
if [[ `uname -m` == 'aarch64' || `uname -m` == 'arm64' ]]; then
    echo "Detected ARM architecture"
    PROCESSOR="aarch64"
    SEATSERVICE_BINARY_NAME="bin_vservice-seat_aarch64_release.tar.gz"
else
    echo "Detected x86_64 architecture"
    PROCESSOR="x86_64"
    SEATSERVICE_BINARY_NAME="bin_vservice-seat_x86_64_release.tar.gz"
fi
SEATSERVICE_EXEC_PATH="$SEATSERVICE_ASSET_FOLDER/$PROCESSOR/target/$PROCESSOR/release/install/bin"

if [[ ! -f "$SEATSERVICE_EXEC_PATH/val_start.sh" ]]
then
  DOWNLOAD_URL=https://github.com/eclipse/kuksa.val.services/releases/download
  echo "Downloading seatservice:$SEATSERVICE_VERSION"
  curl -o $SEATSERVICE_ASSET_FOLDER/$PROCESSOR/$SEATSERVICE_BINARY_NAME --create-dirs -L -H "Accept: application/octet-stream" "$DOWNLOAD_URL/$SEATSERVICE_VERSION/$SEATSERVICE_BINARY_NAME"
  tar -xf $SEATSERVICE_ASSET_FOLDER/$PROCESSOR/$SEATSERVICE_BINARY_NAME -C $SEATSERVICE_ASSET_FOLDER/$PROCESSOR
fi

export DAPR_GRPC_PORT=$SEATSERVICE_GRPC_PORT
export CAN=cansim
export VEHICLEDATABROKER_DAPR_APP_ID=vehicledatabroker

if [ $1 == "DAPR" ]; then
  echo "Run Dapr ...!"
  dapr run \
    --app-id seatservice \
    --app-protocol grpc \
    --app-port $SEATSERVICE_PORT \
    --dapr-grpc-port $SEATSERVICE_GRPC_PORT \
    --components-path $ROOT_DIRECTORY/.dapr/components \
    --config $ROOT_DIRECTORY/.dapr/config.yaml & \
    $SEATSERVICE_EXEC_PATH/val_start.sh
elif [ $1 == "NATIVE" ]; then
  echo "Run native ...!"
  SEATSERVICE_GRPC_PORT='55555'
  export DAPR_GRPC_PORT=$SEATSERVICE_GRPC_PORT
  $SEATSERVICE_EXEC_PATH/val_start.sh
else
  echo "Error: Unsupported middleware type ($1)!"
  exit 1
fi
