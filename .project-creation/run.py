# Copyright (c) 2023 Robert Bosch GmbH

# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# SPDX-License-Identifier: Apache-2.0

import argparse
import json
import os
from pathlib import Path
import shutil


def copy_files(root_destination: str):
    with open(f"{os.path.dirname(__file__)}/config.json") as f:
        files = json.load(f)["files"]
        for file in files:
            destination = root_destination

            if ".project-creation" in file:
                destination = os.path.join(
                    root_destination,
                    os.path.dirname(file.removeprefix(".project-creation/")),
                )

            Path(destination).mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                f"{Path(os.path.dirname(__file__)).parent}/{file}", destination
            )


def copy_example(example_name: str, repo_root: str):
    example_path = os.path.join(
        Path(os.path.dirname(__file__)).parent, "examples", example_name
    )
    app_path = os.path.join(repo_root, "app")

    shutil.copytree(example_path, app_path, dirs_exist_ok=True)


def main():
    parser = argparse.ArgumentParser("run")
    parser.add_argument(
        "-d",
        "--destination",
        type=str,
        required=True,
        help="Path to the root of the repository.",
    )
    parser.add_argument(
        "-e",
        "--example",
        type=str,
        required=False,
        help="Copy the given example to the new repo.",
    )
    args = parser.parse_args()
    copy_files(args.destination)
    if args.example:
        copy_example(args.example, args.destination)


if __name__ == "__main__":
    main()
