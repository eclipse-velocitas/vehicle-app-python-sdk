#!/bin/bash
# Copyright (c) 2022-2025 Contributors to the Eclipse Foundation
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
echo "### Running MQTT Broker                             ###"
echo "#######################################################"

ROOT_DIRECTORY=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/../.." )
source $ROOT_DIRECTORY/.vscode/scripts/exec-check.sh "$@" $(basename $BASH_SOURCE .sh)

MOSQUITTO_IMAGE=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .mosquitto.image | tr -d '"')
MOSQUITTO_TAG=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .mosquitto.version | tr -d '"')

#Terminate existing running services
RUNNING_CONTAINER=$(docker ps | grep "$MOSQUITTO_IMAGE" | awk '{ print $1 }')
if [ -n "$RUNNING_CONTAINER" ];
then
    docker container stop $RUNNING_CONTAINER
fi

docker run --rm --init --name mqtt-broker -p 1883:1883 -p 9001:9001 --network host $MOSQUITTO_IMAGE:$MOSQUITTO_TAG mosquitto -c /mosquitto-no-auth.conf
