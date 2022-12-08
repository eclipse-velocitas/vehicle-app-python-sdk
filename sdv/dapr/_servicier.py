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

import asyncio
import logging
from typing import Callable, Dict, List, Optional, Tuple

import grpc
from cloudevents.sdk.event import v1  # type: ignore
from dapr.proto import appcallback_service_v1, appcallback_v1  # type: ignore
from google.protobuf import empty_pb2

logger = logging.getLogger(__name__)

TopicSubscribeCallable = Callable[[object, v1.Event], None]

DELIMITER = ":"


class Rule:
    """A rule for a subscription."""

    def __init__(self, match: str, priority: int) -> None:
        self.match = match
        self.priority = priority


class _RegisteredSubscription:
    def __init__(
        self,
        subscription: appcallback_v1.TopicSubscription,
        rules: List[Tuple[int, appcallback_v1.TopicRule]],
    ):
        self.subscription = subscription
        self.rules = rules


class _CallbackServicer(appcallback_service_v1.AppCallbackServicer):
    def __init__(self):
        self._topic_map: Dict[str, TopicSubscribeCallable] = {}

        self._registered_topics_map: Dict[str, _RegisteredSubscription] = {}
        self._registered_topics: List[appcallback_v1.TopicSubscription] = []
        self._main_event_loop = asyncio.get_event_loop()

    def register_topic(
        self,
        pubsub_name: str,
        topic: str,
        callback: TopicSubscribeCallable,
        metadata: Optional[Dict[str, str]],
        rule: Optional[Rule] = None,
    ) -> None:
        """Registers topic subscription for pubsub."""
        logger.debug("Registering topic '%s'", topic)
        topic_key = pubsub_name + DELIMITER + topic
        pubsub_topic = topic_key + DELIMITER
        if rule is not None:
            path = getattr(callback, "__name__", rule.match)
            pubsub_topic = pubsub_topic + path
        if pubsub_topic in self._topic_map:
            raise ValueError(f"{topic} is already registered with {pubsub_name}")
        self._topic_map[pubsub_topic] = callback

        registered_topic = self._registered_topics_map.get(topic_key)
        sub: appcallback_v1.TopicSubscription = appcallback_v1.TopicSubscription()
        rules: List[Tuple[int, appcallback_v1.TopicRule]] = []
        if not registered_topic:
            sub = appcallback_v1.TopicSubscription(
                pubsub_name=pubsub_name,
                topic=topic,
                metadata=metadata,
                routes=appcallback_v1.TopicRoutes(),
            )
            registered_topic = _RegisteredSubscription(sub, rules)
            self._registered_topics_map[topic_key] = registered_topic
            self._registered_topics.append(sub)

        sub = registered_topic.subscription
        rules = registered_topic.rules

        if rule:
            path = getattr(callback, "__name__", rule.match)
            rules.append(
                (rule.priority, appcallback_v1.TopicRule(match=rule.match, path=path))
            )
            rules.sort(key=lambda x: x[0])
            topic_rules = [rule for id, rule in rules]
            del sub.routes.rules[:]
            sub.routes.rules.extend(topic_rules)

    def ListTopicSubscriptions(self, request, context):
        return appcallback_v1.ListTopicSubscriptionsResponse(
            subscriptions=self._registered_topics
        )

    def OnTopicEvent(self, request, context):
        pubsub_topic = (
            request.pubsub_name + DELIMITER + request.topic + DELIMITER + request.path
        )
        if pubsub_topic not in self._topic_map:
            context.set_code(grpc.StatusCode.UNIMPLEMENTED)  # type: ignore
            logger.error(
                "topic %s is not implemented allowed topics are %s",
                request.topic,
                self._topic_map,
            )
            raise NotImplementedError(f"topic {request.topic} is not implemented!")

        method: TopicSubscribeCallable = self._topic_map[pubsub_topic]
        if asyncio.iscoroutinefunction(method):
            asyncio.run_coroutine_threadsafe(  # type: ignore
                coro=method(request.data), loop=self._main_event_loop  # type: ignore
            )  # type: ignore
        else:
            # This calls the method on the worker_thread rather than the main thread
            method(request.data)  # type: ignore

        return empty_pb2.Empty()
