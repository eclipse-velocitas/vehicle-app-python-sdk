#!/bin/bash
# Copyright (c) 2022-2026 Contributors to the Eclipse Foundation
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
echo "### Get, build, and install vehicle model           ###"
echo "#######################################################"

ROOT_DIRECTORY=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/../.." )

echo ""
echo "Build vehicle model"
echo "-------------------"
REMOTE_VSS_FILE=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .vss_model.vss_file | tr -d '"')
REMOTE_UNITS_FILE=$(cat $ROOT_DIRECTORY/prerequisite_settings.json | jq .vss_model.units_file | tr -d '"')
LOCAL_VSS_FOLDER=$ROOT_DIRECTORY/.vscode/scripts/assets/vss_data
LOCAL_VSS_FILE=$LOCAL_VSS_FOLDER/vss.json
LOCAL_UNITS_FILE=$LOCAL_VSS_FOLDER/units.yaml
GEN_MODEL_PATH=$ROOT_DIRECTORY/.vscode/scripts/assets/vehicle_model/

mkdir -p $LOCAL_VSS_FOLDER
wget -O $LOCAL_VSS_FILE $REMOTE_VSS_FILE
wget -O $LOCAL_UNITS_FILE $REMOTE_UNITS_FILE

echo ""
echo "Build vehicle model"
echo "-------------------"
python3 -m velocitas.model_generator.cli $LOCAL_VSS_FILE -u $LOCAL_UNITS_FILE -T $GEN_MODEL_PATH -l python

echo ""
echo "Install vehicle model"
echo "---------------------"
python3 -m pip install $GEN_MODEL_PATH
