#!/usr/bin/env bash
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

#********************************************************************************/
##################################################################################
# Help Function                                                                 #
##################################################################################
Help()
{
   # Display Help
   echo "Simple script that run the example applications."
   echo
   echo "Syntax: ./run-app.sh -a APP_NAME [-d|-n] [-p APP_PORT=50008]"
   echo "options:"
   echo "-a             Option to set the application name from the list of examples directory, the name must match the directory name."
   echo "-d             Run with Dapr middleware (default)."
   echo "-n             Run with native middleware."
   echo "-p             Option to set the application's gRPC port. Default is 50008"
   echo "-h/--help      Help."
   echo
}
ROOT_DIRECTORY=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/.." )

# Get App attributes (Name and Port Number)
APP_PORT=50008
export SDV_MIDDLEWARE_TYPE=dapr
while getopts a:dnp:h flag
do
    case "${flag}" in
        a) APP_NAME=${OPTARG};;
        d) export SDV_MIDDLEWARE_TYPE=dapr;;
        n) export SDV_MIDDLEWARE_TYPE=native;;
        p) APP_PORT=${OPTARG};;
        h) Help
        exit;;
    esac
done

if [ ! -d "$APP_NAME" ]; then
    echo "Can't find the example app $APP_NAME. Please make sure to use the -a flag to specify the app name"
    Help
    exit 0;
fi

# Export the Data broker DAPR_GRPC_PORT
export DAPR_GRPC_PORT=55555

if [ $SDV_MIDDLEWARE_TYPE == "dapr" ]; then
    echo "Run with Dapr ...!"
    DAPR_APP_ID="${APP_NAME//[.,\-,_,' ']/}"
    dapr run \
      --app-id $DAPR_APP_ID \
      --app-protocol grpc \
      --app-port $APP_PORT \
      --config $ROOT_DIRECTORY/.dapr/config.yaml  \
      --resources-path $ROOT_DIRECTORY/.dapr/components \
    -- python3 $APP_NAME/src/main.py
elif [ $SDV_MIDDLEWARE_TYPE == "native" ]; then
    echo "Run native ...!"
    python3 $APP_NAME/src/main.py
else
    echo "Error: Unsupported middleware type '$SDV_MIDDLEWARE_TYPE'!"
    exit 1
fi
