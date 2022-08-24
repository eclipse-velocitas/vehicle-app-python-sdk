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

# syntax=docker/dockerfile:1.2

# Build stage, to create the executable
FROM --platform=$TARGETPLATFORM python:3.9-slim-bullseye as builder

RUN apt-get update && apt-get install -y binutils

COPY ./src /src

# Remove this installation for Arm64 once staticx has a prebuilt wheel for Arm64
RUN /bin/bash -c 'set -ex && \
    ARCH=`uname -m` && \
    if [ "$ARCH" == "aarch64" ]; then \
        echo "ARM64" && \
        apt-get install -y gcc && \
        pip3 install --no-cache-dir scons; \
    fi'

RUN apt-get install -y git
RUN pip3 install --no-cache-dir pyinstaller \
    && pip3 install --no-cache-dir patchelf \
    && pip3 install --no-cache-dir staticx \
    && pip3 install --no-cache-dir -r src/requirements.txt \
    && pip3 install --no-cache-dir -r src/requirements-links.txt

WORKDIR /src

RUN pyinstaller --clean -F -s VehicleApp/main.py

WORKDIR /src/dist

RUN staticx main run-exe

# Runner stage, to copy the executable
FROM scratch

COPY --from=builder ./src/dist/run-exe /dist/

WORKDIR /tmp
WORKDIR /dist

ENV PATH="/dist:$PATH"

LABEL org.opencontainers.image.source="https://github.com/eclipse-velocitas/vehicle-app-python-template"

CMD ["./run-exe"]