# How to Contribute to Eclipse Velocitas Vehicle App SDK for Python

First of all, thanks for considering to contribute to Eclipse Velocitas. We really
appreciate the time and effort you want to spend helping to improve things around here.

In order to get you started as fast as possible we need to go through some organizational issues first, though.

## Eclipse Contributor Agreement

Before your contribution can be accepted by the project team contributors must
electronically sign the Eclipse Contributor Agreement (ECA).

* http://www.eclipse.org/legal/ECA.php

Commits that are provided by non-committers must have a Signed-off-by field in
the footer indicating that the author is aware of the terms by which the
contribution has been provided to the project. The non-committer must
additionally have an Eclipse Foundation account and must have a signed Eclipse
Contributor Agreement (ECA) on file.

For more information, please see the Eclipse Committer Handbook:
https://www.eclipse.org/projects/handbook/#resources-commit

## Code Style Guide
* Use [Black](https://black.readthedocs.io/) to format your code.
* Use [isort](https://isort.readthedocs.io/) to sort imports.
* Use [pydocstyle](https://pydocstyle.readthedocs.io/) to check for PEP-8 style issues.
* Use [mypy](https://mypy.readthedocs.io/) to check for type errors.
* Use [flake8](https://flake8.readthedocs.io/) to check for style issues.
* Above and other tools will run automatically if you install
 [pre-commit](https://pre-commit.com/) using the instructions below.

## Making Your Changes

* Fork the repository on GitHub.
* Create a new branch for your changes.
* Install dependencies:

   ```bash
   pip3 install -r requirements.txt
   ```
* Install package in editable mode:

   ```bash
   pip3 install -e .
   ```
* Make your changes following the code style guide (see Code Style Guide section above).
* When you create new files make sure you include a proper license header at the top of the file (see License Header section below).
* When you make changes to existing protocol buffer files, regenerate the python descriptors with the following command:

   ```bash
   ./generate-grpc-stubs.sh
   ```
   or use the corresponding VSCode task.
* Make sure you include test cases and new examples for non-trivial features.
* Make sure test cases provide sufficient code coverage (see GitHub actions for minimal accepted coverage).
* Install and run [pre-commit](https://pre-commit.com/) to automatically check for style guide issues.
    ```bash
    pre-commit install
    pre-commit run --all-files
    ```
    > **_NOTE:_** Or just use task `Local - Pre Commit Action` by pressing `F1` and select `Tasks - Run Task`
* Make sure the unit and integration test suites passes after your changes.
    ```bash
    tox -e py38
    ```
* Add new examples for non-trivial features.
* Commit your changes into that branch.
* Use descriptive and meaningful commit messages. Start the first line of the commit message with the issue number and title e.g. `[#9865] Add token based authentication`.
* Squash multiple commits that are related to each other semantically into a single one.
* Make sure you use the `-s` flag when committing as explained above.
* Push your changes to your branch in your forked repository.

## Python Dependency Management

In this project, the [pip-tools](https://github.com/jazzband/pip-tools) are used to manage the python dependencies and to keep all packages up-to-date.

The required pip-based dependencies of this project are defined in the [setup.py](./setup.py). All runtime dependencies are listed in the `"install_requires"` while the development dependencies are listed in the `[dev]` section of the `"extras_require"`. In other words:
* The requirements that are defined in the `"install_requires"` are only installed when using the Vehicle app SDK as a runtime dependency for vehicle app development.
* The requirements that are defined in the `"extras_require[dev]"` are installed for the contribution of the Vehicle app SDK development within the dev-container or in a dedicated virtual environments. This list consists of all the necessary runtime, testing and development tools packages and need to be installed before start contributing to the project.

The process for the dependency management of this project can be summarized as following:
* The `pip-compile` tool will generate the [requirements.txt](./requirements.txt). By executing this tools, the `"requirements.txt"` file will be updated with all underlying dependencies. The command below shall be executed every time a new python package is added to the project and/or to bump the package versions.

   ```bash
   pip-compile --extra=dev
   ```
* Please run the `pip-compile` with `-U` flag in order to force update all packages with the latest versions. However, you need to make sure when force updating all packages that everything works as expected.
   ```bash
   pip-compile --extra=dev -U
   ```
* Run `pip-sync` or `pip install` to install the required dependencies from the [requirements.txt](./requirements.txt) alternatively.
   ```bash
   pip-sync
   ```
   ```bash
   pip3 install -r requirements.txt
   ```
If there are any other `none public python dependencies` (E.g. GitHub links), they shall not be added to the setup.py file directly. Instead, they must be added to the [requirements-links.txt](./requirements-links.txt).

> **_NOTE:_** `Please don't try to update the versions of the dependencies manually.`

## License Header

Please make sure any file you newly create contains a proper license header like this:

```python
# Copyright (c) 2023 Contributors to the Eclipse Foundation
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
```
Please adjusted the comment character to the specific file format.

## Submitting the Changes

Submit a pull request via the normal GitHub UI.

## After Submitting

* Do not use your branch for any other development, otherwise further changes that you make will be visible in the PR.
