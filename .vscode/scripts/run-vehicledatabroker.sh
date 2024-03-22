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
echo "### Running Databroker                              ###"
echo "#######################################################"

ROOT_DIRECTORY=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/../.." )
source $ROOT_DIRECTORY/.vscode/scripts/exec-check.sh "$@" $(basename $BASH_SOURCE .sh)

DATABROKER_IMAGE=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .databroker.image | tr -d '"')
DATABROKER_TAG=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .databroker.version | tr -d '"')

RUNNING_CONTAINER=$(docker ps | grep "$DATABROKER_IMAGE" | awk '{ print $1 }')
if [ -n "$RUNNING_CONTAINER" ];
then
    docker container stop $RUNNING_CONTAINER
fi

VSPEC_FILE_PATH=$ROOT_DIRECTORY/.vscode/scripts/broker_config/vss_rel_3.0.json
KUKSA_DATA_BROKER_PORT='55555'
#export RUST_LOG="info,databroker=debug,vehicle_data_broker=debug"

if [ $1 == "NATIVE" ]; then
  echo "Run native ...!"
  docker run \
    -v $VSPEC_FILE_PATH:$VSPEC_FILE_PATH \
    -e KUKSA_DATA_BROKER_METADATA_FILE=$VSPEC_FILE_PATH \
    -e KUKSA_DATA_BROKER_PORT \
    -e RUST_LOG \
    --network host \
    $DATABROKER_IMAGE:$DATABROKER_TAG
else
  echo "Error: Unsupported middleware type ($1)!"
  exit 1
fi
