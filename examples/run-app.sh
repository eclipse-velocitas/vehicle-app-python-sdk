#!/usr/bin/env bash
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

#********************************************************************************/
##################################################################################
# Help Function                                                                 #
##################################################################################
Help()
{
   # Display Help
   echo "Simple script that run the example applications."
   echo
   echo "Syntax: ./run-app.sh -a APP_NAME [-n]"
   echo "options:"
   echo "-a             Option to set the application name from the list of examples directory, the name must match the directory name."
   echo "-n             Run with native middleware (default)."
   echo "-h/--help      Help."
   echo
}
ROOT_DIRECTORY=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/.." )

# Get App attributes (Name and Port Number)
export SDV_MIDDLEWARE_TYPE=native
while getopts a:dnp:h flag
do
    case "${flag}" in
        a) APP_NAME=${OPTARG};;
        n) export SDV_MIDDLEWARE_TYPE=native;;
        h) Help
        exit;;
    esac
done

if [ ! -d "$APP_NAME" ]; then
    echo "Can't find the example app $APP_NAME. Please make sure to use the -a flag to specify the app name"
    Help
    exit 0;
fi

if [ $SDV_MIDDLEWARE_TYPE == "native" ]; then
    echo "Run native ...!"
    export SDV_MQTT_ADDRESS="mqtt://localhost:1883"
    export SDV_VEHICLEDATABROKER_ADDRESS="grpc://localhost:55555"
    export SDV_SEATSERVICE_ADDRESS="grpc://localhost:50051"
    export SDV_HVACSERVICE_ADDRESS="grpc://localhost:50052"
    python3 $APP_NAME/src/main.py
else
    echo "Error: Unsupported middleware type '$SDV_MIDDLEWARE_TYPE'!"
    exit 1
fi
