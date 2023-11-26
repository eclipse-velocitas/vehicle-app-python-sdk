#!/bin/bash
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

echo "#######################################################"
echo "### Running Seat Service                            ###"
echo "#######################################################"

ROOT_DIRECTORY=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/../.." )
source $ROOT_DIRECTORY/.vscode/scripts/exec-check.sh "$@" $(basename $BASH_SOURCE .sh)

SEATSERVICE_IMAGE=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .seatservice.image | tr -d '"')
SEATSERVICE_TAG=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .seatservice.version | tr -d '"')

RUNNING_CONTAINER=$(docker ps | grep "$SEATSERVICE_IMAGE" | awk '{ print $1 }')
if [ -n "$RUNNING_CONTAINER" ];
then
    docker container stop $RUNNING_CONTAINER
fi

export VEHICLEDATABROKER_DAPR_APP_ID=vehicledatabroker
export VEHICLEDATABROKER_NATIVE_PORT=55555
export SERVICE_PORT=50051
export CAN=cansim

if [ $1 == "DAPR" ]; then
  echo "Run with Dapr ...!"
  dapr run \
    --app-id seatservice \
    --app-protocol grpc \
    --app-port $SERVICE_PORT \
    --resources-path $ROOT_DIRECTORY/.dapr/components \
    --config $ROOT_DIRECTORY/.dapr/config.yaml \
  -- docker run \
    -e VEHICLEDATABROKER_DAPR_APP_ID \
    -e DAPR_GRPC_PORT \
    -e DAPR_HTTP_PORT \
    -e SERVICE_PORT \
    -e CAN \
    --network host \
    $SEATSERVICE_IMAGE:$SEATSERVICE_TAG
elif [ $1 == "NATIVE" ]; then
  echo "Run native ...!"
  docker run \
    -e DAPR_GRPC_PORT=$VEHICLEDATABROKER_NATIVE_PORT \
    -e SERVICE_PORT \
    -e CAN \
    --network host \
    $SEATSERVICE_IMAGE:$SEATSERVICE_TAG
else
  echo "Error: Unsupported middleware type ($1)!"
  exit 1
fi
