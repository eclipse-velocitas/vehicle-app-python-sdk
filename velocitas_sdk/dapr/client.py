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

"""" dapr gateway"""

import asyncio
import logging
import os
import urllib.request
from http import HTTPStatus
from urllib.error import HTTPError

import grpc
from dapr.proto import api_service_v1, api_v1  # type: ignore

from velocitas_sdk.dapr.locator import DAPR_PUB_SUB_NAME_VALUE

logger = logging.getLogger(__name__)


def publish_mqtt_event(topic: str, data: str) -> None:
    """Publishes an event to the specified MQTT topic over dapr pub/sub."""
    port = int(str(os.getenv("DAPR_GRPC_PORT")))
    address = f"localhost:{port}"
    channel = grpc.insecure_channel(address)
    dapr_stub = api_service_v1.DaprStub(channel)
    req = api_v1.PublishEventRequest(
        pubsub_name=DAPR_PUB_SUB_NAME_VALUE,
        topic=topic,
        data=bytes(data, "utf-8"),
        metadata={"rawPayload": "true"},
    )
    dapr_stub.PublishEvent(req)
    logger.debug(
        "Published an event data :%s to the specified MQTT topic: %s", data, topic
    )


async def wait_for_sidecar() -> None:
    """Poll dapr sidecar health check endpoint until it returns 204 NO_CONTENT.
    GRPC proxy requests are only allowed after dapr sidecar is ready."""

    success = False
    while not success:
        port = os.getenv("DAPR_HTTP_PORT")
        if port is not None:
            target_port = int(str(os.getenv("DAPR_HTTP_PORT")))
            try:
                response = urllib.request.urlopen(  # nosec
                    f"http://localhost:{target_port}/v1.0/healthz"
                )
                response.read()
                success = response.status == HTTPStatus.NO_CONTENT
                logger.debug(
                    "dapr: Health endpoint returned status code: %s", response.status
                )
            except HTTPError as error:
                if error.code == HTTPStatus.INTERNAL_SERVER_ERROR:
                    logger.info("Waiting for dapr sidecar...")
                else:
                    logger.error("Unexpected error from dapr sidecar: %d", error.code)
                await asyncio.sleep(0.1)
            except BaseException as error:
                logger.error("%s", str(error))
                await asyncio.sleep(0.1)
        else:
            await asyncio.sleep(0.1)
