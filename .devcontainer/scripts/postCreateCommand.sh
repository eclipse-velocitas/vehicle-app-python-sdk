# This file is maintained by velocitas CLI, do not modify manually. Change settings in .velocitas.json
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
echo "### Run VADF Lifecycle Management                   ###"
echo "#######################################################"
velocitas init
velocitas sync

echo "#######################################################"
echo "### Executing add-python.sh                         ###"
echo "#######################################################"
.devcontainer/scripts/add-python.sh 2>&1 | tee -a $HOME/add-python.log

echo "#######################################################"
echo "### Install python requirements                     ###"
echo "#######################################################"
REQUIREMENTS="./requirements.txt"
if [ -f $REQUIREMENTS ]; then
    pip3 install -r $REQUIREMENTS
fi
REQUIREMENTS="./requirements-links.txt"
if [ -f $REQUIREMENTS ]; then
    pip3 install -r $REQUIREMENTS
fi

pip3 install -e .

# add repo to git safe.directory
REPO=$(pwd)
git config --global --add safe.directory $REPO
