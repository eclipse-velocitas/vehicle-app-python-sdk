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
echo "### Running HVAC Service                            ###"
echo "#######################################################"

ROOT_DIRECTORY=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/../.." )
source $ROOT_DIRECTORY/.vscode/scripts/exec-check.sh "$@" $(basename $BASH_SOURCE .sh)

HVACSERVICE_IMAGE=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .hvacservice.image | tr -d '"')
HVACSERVICE_TAG=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .hvacservice.version | tr -d '"')

RUNNING_CONTAINER=$(docker ps | grep "$HVACSERVICE_IMAGE" | awk '{ print $1 }')
if [ -n "$RUNNING_CONTAINER" ];
then
    docker container stop $RUNNING_CONTAINER
fi

export VEHICLEDATABROKER_NATIVE_PORT=55555
export SERVICE_PORT=50052

echo "Run native ...!"
docker run \
  -e VDB_ADDRESS="127.0.0.1:$VEHICLEDATABROKER_NATIVE_PORT" \
  -e HVAC_ADDR="0.0.0.0:${SERVICE_PORT}" \
  --network host \
  $HVACSERVICE_IMAGE:$HVACSERVICE_TAG
