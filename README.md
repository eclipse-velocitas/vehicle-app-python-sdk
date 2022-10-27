# Vehicle App Python Sdk

[![CI workflow](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/actions/workflows/ci.yaml/badge.svg)](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/actions/workflows/ci.yaml)
[![License: Apache](https://img.shields.io/badge/License-Apache-yellow.svg)](http://www.apache.org/licenses/LICENSE-2.0)

The Vehicle App SDK for Python allows to create `Vehicle Apps` from the [Velocitas](https://github.com/eclipse-velocitas/velocitas-docs) development model in the Python programming language.

This includes the following packages:

* [sdv.model](./sdv/model.py) - Vehicle Model ontology
* [sdv.dapr](./sdv/dapr) - Dapr middleware integration
* [sdv.conf](./sdv/conf.py) - Vehicle App configuration
* [sdv.vehicle_app](./sdv/vehicle_app.py) - Vehicle App abstraction
* [sdv.vdb](./sdv/vdb) - Vehicle Data Broker integration
* [sdv.test](./sdv/test) - Integration test support
* [sdv.util](./sdv/util) - Logging and other utilities

## Status

> Note: The Vehicle App Python SDK is currently under active development in alpha phase.

## Prerequisites

- Python 3.8 or later is required to use this package.

## Install the package

Install the Vehicle App Python SDK with pip:

```bash
pip install git+https://github.com/eclipse-velocitas/vehicle-app-python-sdk.git@<version>
```

## Documentation

* [Runtime Services (local execution)](https://eclipse-velocitas.github.io/velocitas-docs/docs/tutorials/vehicle-app-runtime/run_runtime_services_locally/): Using runtime services (like _Vehicle Data Broker_ or _Vehicle Services_) in the development environment.
* [Runtime Services (Kubernetes execution)](https://eclipse-velocitas.github.io/velocitas-docs/docs/tutorials/vehicle-app-runtime/run_runtime_services_kubernetes/): Using runtime services (like _Vehicle Data Broker_ or _Vehicle Services_) in Kubernetes (K3D) environment.
* [Velocitas Development Model](https://eclipse-velocitas.github.io/velocitas-docs/docs/concepts/development_model/): Creating Vehicle App and Vehicle Models with the Python SDK
* [Integration Tests](https://eclipse-velocitas.github.io/velocitas-docs/docs/tutorials/integration_tests/): Running and developing integration tests

## Python Vehicle App SDK Examples

These examples demonstrate how to use the Python Vehicle App SDK:

| Example | Description |
|---------|-------------|
| [Dynamic Rule](./examples/dynamic-rule/) | Create a Vehicle Data Broker rule with the fluent query methods.
| [Seat Adjuster](./examples/seat-adjuster/) | Seat-Adjuster App that demonstrates MQTT communication and invocation of a Vehicle Service over gRPC.
| [Dog Mode](./examples/dog-mode//) | Dog-Mode App that demonstrates MQTT communication and invocation of a Vehicle Service over gRPC, the app also subscribes for vehicle data points and sets the cabin temperature.
| [Static Rule](./examples/static-rule/) | Create a Vehicle Data Broker rule with the subscribe_to_data_point annotation.
| [VDB Queries](./examples/vdb-queries/) | Demonstrates various aspects of creating Vehicle Data Broker queries.
| [Array Datatype](./examples/array-datatype/) | Shows a Vehicle Data Broker query that returns an array data point.
| [DataPoint-Set](./examples/datapoint-set/) | Shows how to set the value of the datapoint actuator value API.

## Contribution
- [GitHub Issues](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/issues)
- [Mailing List](https://accounts.eclipse.org/mailing-list/velocitas-dev)
- [Contribution](./CONTRIBUTING.md/)
