# Vehicle App Python Sdk

[![CI workflow](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/actions/workflows/ci.yaml/badge.svg)](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/actions/workflows/ci.yaml)
[![License: Apache](https://img.shields.io/badge/License-Apache-yellow.svg)](http://www.apache.org/licenses/LICENSE-2.0)

The `Vehicle App SDK` reduces the effort required to implement Vehicle Apps by using the Velocitas development model for the Python programming language. To create a Vehicle App, please use our [Vehicle App Template](https://github.com/eclipse-velocitas/vehicle-app-python-template) which uses this sdk.

The Vehicle App Python SDK includes the following packages:

* [velocitas_sdk.vehicle_app](./velocitas_sdk/vehicle_app.py) - Vehicle App abstraction
* [velocitas_sdk.model](./velocitas_sdk/model.py) - Vehicle Model ontology
* [velocitas_sdk.config](./velocitas_sdk/config.py) - Vehicle App configuration
* [velocitas_sdk.base](./velocitas_sdk/base.py) - Base classes for middleware abstraction
* [velocitas_sdk.native](./velocitas_sdk/native) - Native middleware definition
* [velocitas_sdk.vdb](./velocitas_sdk/vdb) - Vehicle Data Broker integration
* [velocitas_sdk.test](./velocitas_sdk/test) - Integration test support
* [velocitas_sdk.util](./velocitas_sdk/util) - Logging and other utilities

## Status

> Note: The Vehicle App Python SDK is currently under active development in alpha phase.

The Vehicle App Python SDK starting from version 0.16.0 has been migrated to use the `kuksa.val.v2` API
of the KUKSA Databroker. You'll need a KUKSA Databroker version >= 0.5.0 supporting this API.

The usage of the `sdv.databroker.v1` API is completely removed from this SDK now. Its support by the
KUKSA Databroker was deprecated already for a long time and was recently removed there. Be aware that
the support for conditions within subscription queries is also removed with that migration.

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
| [Annotation Subscribe](./examples/static-rule/) | Create a Vehicle Data Broker rule with the subscribe_to_data_point annotation.
| [Array Datatype](./examples/array-datatype/) | Shows a Vehicle Data Broker query that returns an array data point.
| [Atomic Set](./examples/atomic-set/) | Shows how to set the values of multiple datapoint actuators in one "atomic" step.
| [DataPoint Set](./examples/datapoint-set/) | Shows how to set the value of the datapoint actuator value API.
| [Dog Mode](./examples/dog-mode//) | Dog-Mode App that demonstrates MQTT communication and invocation of a Vehicle Service over gRPC, the app also subscribes for vehicle data points and sets the cabin temperature.<br>__This is kept for "viewing" but is not executable. Requires migration to the current state of KUKSA and Velocitas.__
| ~~[Dynamic Rule](./examples/dynamic-rule/)~~ | ~~Create a Vehicle Data Broker rule with the fluent query methods.~~<br>Removed as queries with conditions aren't supported by `kuksa.val.v2`.
| ~~[Static Rule](./examples/static-rule/)~~ | ~~Create a Vehicle Data Broker rule with the subscribe_to_data_point annotation.~~<br>Removed as queries with conditions aren't supported by `kuksa.val.v2`.
| ~~[VDB Queries](./examples/vdb-queries/)~~ | ~~Demonstrates various aspects of creating Vehicle Data Broker queries.~~<br>Removed as queries with conditions aren't supported by `kuksa.val.v2`.
| [Seat Adjuster](./examples/seat-adjuster/) | Seat-Adjuster App that demonstrates MQTT communication and seat control via actuator data points.<br>:point_right: This example can only be run from the [Vehicle App Template](https://github.com/eclipse-velocitas/vehicle-app-python-template). :point_left:
| [Subscribe Multiple](./examples/static-rule/) | Subscribe to multiple signals with a single subscription.

### Prerequisites

Before the examples can be executed you need to install a generated vehicle model based on a VSS signal catalogue
of version 4 or newer. To build and install that model, please do the following steps:

1. Install the Velocitas model generator:
```bash
python3 -m pip install velocitas-model-generator
```

2. Run the vscode task "Build and install vehicle model". (E.g. press Ctrl+Shift+P, choose "Tasks: Run Task" ->
   "Build and install vehicle model".)

### Run an example

All examples (except the Seat Adjuster) can be run via
```bash
cd examples
./run-app.sh -a <example-folder-name>
```
By default the examples are started using the native middleware.

## Contribution
- [GitHub Issues](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/issues)
- [Mailing List](https://accounts.eclipse.org/mailing-list/velocitas-dev)
- [Contribution](./CONTRIBUTING.md/)

### Creating a new release

1. Update examples

This repository contain some example requirement files that reference the `velocitas-sdk` package created when we release the repository.
Update `velocitas-sdk` version number in the following files:

* `.project-creation/.skeleton/requirements-velocitas.txt`
* `examples/seat-adjuster/requirements-velocitas.txt`

Use the version number intended to be used for the release.

2. Create a PR with the required changes

> Note: The [project creation workflow](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/actions/workflows/project-creation.yaml) will fail, since the new tag is required by the workflow but not yet available. Since these checks are not mandatory to be able to merge the PR, you can still release your changes.

3. Once the PR is merged: Tag the commit and upload to GitHub

Create a release in the GitHub UI and use the new tag of the form `vX.Y.X`.
That will trigger the [release](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/actions/workflows/release.yaml) workflow.
If the action is successfully executed a new version of `velocitas-sdk` is published in [PyPI](https://pypi.org/project/velocitas-sdk/).

4. Re-run project creation tests

Now, when the updated [PyPI](https://pypi.org/project/velocitas-sdk/) package exists, the [project creation workflow](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/actions/workflows/project-creation.yaml) is expected to succeed if run manually for `main`.
If not you need to troubleshoot why it doesn't.

### Updating Dependencies

This repository specifies exact Python versions  in `setup.py` and other files.
If a version needs to be updated, for example if a vulnerability is detected, the following approach needs to be followed

1. Update version in `setup.py` if needed
2. Update generated requirement files.

```bash
pip-compile -U --extra=dev
```

3. Update version in `examples/seat-adjuster/requirements.in` if needed
4. Update generated file for Seat Adjuster

```bash
cd examples/seat-adjuster
pip-compile -U
```

5. Update version in `.project-creation/.skeleton/requirements.in` if needed
6. Update generated file for Skeleton

```bash
cd .project-creation/.skeleton/
pip-compile -U
```

7. Update `NOTICE-3RD-PARTY-CONTENT.md`

The easiest way to do it is to create a Pull Request.
Then the [check license workflow](https://github.com/eclipse-velocitas/vehicle-app-python-sdk/actions/workflows/check-licenses.yml) will fail as versions used no longer match versions stated in the file.
Copy output from the workflow to the `NOTICE-3RD-PARTY-CONTENT.md` file and update the Pull Request.

8. Update examples and create a new release

As we explicitly use our "own" PyPI package we need to udpate references and create a new release, see release section above.
