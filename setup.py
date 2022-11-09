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

from setuptools import setup

requirements = [
    "grpcio>=1.44.0",
    "protobuf>=3.19.4",
    "dapr>=1.6.0",
    "paho-mqtt>=1.6.1",
    "opentelemetry-api>=1.11.1",
    "opentelemetry-sdk>=1.11.1",
    "opentelemetry-distro>=0.31b0",
    "opentelemetry-instrumentation-logging>=0.31b0",
]

extra_requirements = {
    "dev": [
        ##########################################
        # Runtime Packages
        ##########################################
        "protobuf",
        "grpcio",
        "dapr",
        "cloudevents",
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
        "pydocstyle",
        "black",
        "pylint",
        "mypy",
        "bandit",
        "flake8",
        "flake8-bugbear",
        "flake8-builtins",
        "pip-tools",
    ]
}

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sdv",
    version="0.7.2",
    description="A Python SDK for Vehicle app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eclipse-velocitas/vehicle-app-python-sdk",
    packages=[
        "sdv",
        "sdv.util",
        "sdv.dapr",
        "sdv.pubsub",
        "sdv.proto",
        "sdv.proto.chariott.common.v1",
        "sdv.proto.chariott.runtime.v1",
        "sdv.vdb",
        "sdv.test",
        "sdv_examples.seat-adjuster",
    ],
    package_dir={
        "sdv_examples.seat-adjuster": "examples/seat-adjuster",
    },
    package_data={"sdv": ["py.typed"]},
    include_package_data=True,
    install_requires=requirements,
    extras_require=extra_requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
