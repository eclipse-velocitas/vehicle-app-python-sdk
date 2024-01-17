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
set -e

echo "#######################################################"
echo "### Running FeederCan                               ###"
echo "#######################################################"

ROOT_DIRECTORY=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/../.." )
source $ROOT_DIRECTORY/.vscode/scripts/exec-check.sh "$@" $(basename $BASH_SOURCE .sh)

FEEDERCAN_IMAGE=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .feedercan.image | tr -d '"')
FEEDERCAN_TAG=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .feedercan.version | tr -d '"')

RUNNING_CONTAINER=$(docker ps | grep "$FEEDERCAN_IMAGE" | awk '{ print $1 }')
if [ -n "$RUNNING_CONTAINER" ];
then
    docker container stop $RUNNING_CONTAINER
fi

export VEHICLEDATABROKER_DAPR_APP_ID=vehicledatabroker
export DATABROKER_NATIVE_PORT=55555
export LOG_LEVEL=info,databroker=info,dbcfeeder.broker_client=debug,dbcfeeder=debug
export USECASE="databroker"

if [ $2 == "DOGMODE" ]; then
  echo "Use DogMode feeder config ...!"
  CONFIG_DIR="$ROOT_DIRECTORY/.vscode/scripts/feeder_config/dogmode"
  export DBC_FILE="/data/DogMode.dbc"
  export MAPPING_FILE="/data/mapping_DogMode.yml"
  export CANDUMP_FILE="/data/candump_DogMode.log"
else
  echo "Use default feeder config ...!"
  CONFIG_DIR="$ROOT_DIRECTORY/.vscode/scripts/feeder_config/default"
  export DBC_FILE="/data/Model3CAN.dbc"
  export MAPPING_FILE="/data/mapping.yml"
  export CANDUMP_FILE="/data/candump.log"
fi

if [ $1 == "DAPR" ]; then
  echo "Run with Dapr ...!"
  dapr run \
    --app-id feedercan \
    --app-protocol grpc \
    --resources-path $ROOT_DIRECTORY/.dapr/components \
    --config $ROOT_DIRECTORY/.dapr/config.yaml \
  -- docker run \
    -v ${CONFIG_DIR}:/data \
    -e VEHICLEDATABROKER_DAPR_APP_ID \
    -e DAPR_GRPC_PORT \
    -e DAPR_HTTP_PORT \
    -e LOG_LEVEL \
    -e USECASE \
    -e CANDUMP_FILE \
    -e DBC_FILE \
    -e MAPPING_FILE \
    --network host \
    $FEEDERCAN_IMAGE:$FEEDERCAN_TAG
elif [ $1 == "NATIVE" ]; then
  echo "Run native ...!"
  docker run \
    -v ${CONFIG_DIR}:/data \
    -e DAPR_GRPC_PORT=$DATABROKER_NATIVE_PORT \
    -e LOG_LEVEL \
    -e USECASE \
    -e CANDUMP_FILE \
    -e DBC_FILE \
    -e MAPPING_FILE \
    --network host \
    $FEEDERCAN_IMAGE:$FEEDERCAN_TAG
else
  echo "Error: Unsupported middleware type ($1)!"
  exit 1
fi
