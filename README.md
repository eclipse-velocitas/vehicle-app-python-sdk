# Vehicle App Python Sdk

[![CI workflow](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/actions/workflows/ci.yaml/badge.svg)](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/actions/workflows/ci.yaml)
[![License: Apache](https://img.shields.io/badge/License-Apache-yellow.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The `Vehicle App SDK` reduces the effort required to implement Vehicle Apps by using the Velocitas development model for the Python programming language. To create a Vehicle App, please use our [Vehicle App Template](https://github.com/eclipse-velocitas/vehicle-app-python-template) which uses this sdk.

This includes the following packages:

* [sdv.model](./sdv/model.py) - Vehicle Model ontology
* [sdv.dapr](./sdv/dapr) - Dapr middleware integration
* [sdv.conf](./sdv/config.py) - Vehicle App configuration
* [sdv.vehicle_app](./sdv/vehicle_app.py) - Vehicle App abstraction
* [sdv.vdb](./sdv/vdb) - Vehicle Data Broker integration
* [sdv.test](./sdv/test) - Integration test support
* [sdv.util](./sdv/util) - Logging and other utilities

## Status

> Note: The Vehicle App Python SDK is currently under active development in alpha phase.

## Prerequisites

- Python 3.10 or later is required to use this package.

## Install the package

Install the Vehicle App Python SDK with pip:

```bash
pip install git+https://github.com/eclipse-velocitas/vehicle-app-python-sdk.git@<version>
```

## Documentation

* [Velocitas Development Model](https://eclipse.dev/velocitas/docs/concepts/development_model/): Learn more about the Velocitas programming model and the SDK
* [Velocitas Tutorials](https://eclipse.dev/velocitas/docs/tutorials/): Learn how to get started, including setting up the development environment, creating a Vehicle Model as well as developing and deploying a Vehicle App.

## Python Vehicle App SDK Examples

These examples demonstrate how to use the Python Vehicle App SDK:

| Example | Description |
|---------|-------------|
| [Array Datatype](./examples/array-datatype/) | Shows a Vehicle Data Broker query that returns an array data point.
| [Atomic Set](./examples/atomic-set/) | Shows how to set the values of multiple datapoint actuators in one "atomic" step.
| [DataPoint Set](./examples/datapoint-set/) | Shows how to set the value of the datapoint actuator value API.
| [Dog Mode](./examples/dog-mode//) | Dog-Mode App that demonstrates MQTT communication and invocation of a Vehicle Service over gRPC, the app also subscribes for vehicle data points and sets the cabin temperature.
| [Dynamic Rule](./examples/dynamic-rule/) | Create a Vehicle Data Broker rule with the fluent query methods.
| [Static Rule](./examples/static-rule/) | Create a Vehicle Data Broker rule with the subscribe_to_data_point annotation.
| [VDB Queries](./examples/vdb-queries/) | Demonstrates various aspects of creating Vehicle Data Broker queries.
| [Seat Adjuster](./examples/seat-adjuster/) | Seat-Adjuster App that demonstrates MQTT communication and seat control via actuator data points.<br>(i) This example can only be run from the [Vehicle App Template](https://github.com/eclipse-velocitas/vehicle-app-python-template).

All examples (except the Seat Adjuster) can be run via
```bash
cd examples
./run-app.sh -a <example-folder-name>
```
By default the examples are started using the Dapr middleware. If specifying the `-n` flag they are started with native middleware, instead.

## Contribution
- [GitHub Issues](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/issues)
- [Mailing List](https://accounts.eclipse.org/mailing-list/velocitas-dev)
- [Contribution](./CONTRIBUTING.md/)
