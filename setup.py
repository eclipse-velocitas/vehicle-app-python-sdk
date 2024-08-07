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

from setuptools import setup

requirements = [
    "grpcio==1.64.1",
    "protobuf==5.27.2",
    "cloudevents==1.11.0",
    "aiohttp==3.9.5",
    "paho-mqtt==2.1.0",
    "opentelemetry-distro==0.46b0",
    "opentelemetry-instrumentation-logging==0.46b0",
    "opentelemetry-sdk==1.25.0",
    "opentelemetry-api==1.25.0",
]

extra_requirements = {
    "dev": [
        ##########################################
        # Runtime Packages
        ##########################################
        "protobuf",
        "grpcio>=1.59.0",
        "grpcio-tools",
        "grpc-stubs",
        "mypy-protobuf",
        "apscheduler",
        "Deprecated",
        "types-Deprecated",
        ##########################################
        # Testing Packages
        ##########################################
        "pytest",
        "pytest-asyncio",
        "types-mock",
        "pytest-cov",
        "tox",
        ##########################################
        # Development Tools Packages
        ##########################################
        "pre-commit",
        "mypy",
        "pip-tools",
    ]
}

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="velocitas_sdk",
    version="0.15.0",
    description="A Python SDK for Vehicle app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eclipse-velocitas/vehicle-app-python-sdk",
    packages=[
        "velocitas_sdk",
        "velocitas_sdk.util",
        "velocitas_sdk.native",
        "velocitas_sdk.proto",
        "velocitas_sdk.vdb",
        "velocitas_sdk.test",
        "velocitas_examples.seat-adjuster",
    ],
    package_dir={
        "velocitas_examples.seat-adjuster": "examples/seat-adjuster",
    },
    package_data={"velocitas_sdk": ["py.typed"]},
    include_package_data=True,
    install_requires=requirements,
    extras_require=extra_requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
