# Copyright (c) 2022-2025 Contributors to the Eclipse Foundation
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

# type: ignore
import logging
import os
import sys

from opentelemetry import trace
from opentelemetry.instrumentation.logging.constants import DEFAULT_LOGGING_FORMAT
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.trace import INVALID_SPAN_CONTEXT, set_span_in_context

CONTEXT_NAME = "app-context"
context = set_span_in_context(CONTEXT_NAME, context={})
provider = TracerProvider()
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)


def get_opentelemetry_log_format() -> str:
    return DEFAULT_LOGGING_FORMAT


def get_opentelemetry_log_factory():
    return set_opentelemetry_factory_span(
        tracer.start_span(CONTEXT_NAME, context=context)
    )


def get_default_log_format() -> str:
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    return format_str


def get_default_date_format() -> str:
    datefmt = "%m/%d/%Y %I:%M:%S %p"
    return datefmt


def get_log_level() -> str:
    try:
        # loglevel set to ERROR default, in case env variable not found
        loglevel = str(os.getenv("LOGLEVEL", "ERROR")).upper()
        if loglevel not in ["ERROR", "DEBUG", "INFO", "WARNING", "CRITICAL"]:
            raise LogLevelValueError(
                f"Retrieved LOGLEVEL env variable current value is '{loglevel}', \
                it should be among these 'ERROR, DEBUG, INFO, WARNING, CRITICAL'"
            )
        return loglevel
    except Exception as error:
        raise error


def set_opentelemetry_factory_span(span):
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)

        record.otelSpanID = "0"
        record.otelTraceID = "0"
        record.otelTraceSampled = True
        ctx = span.get_span_context()
        if ctx != INVALID_SPAN_CONTEXT:
            record.otelSpanID = format(ctx.span_id, "016x")
            record.otelTraceID = format(ctx.trace_id, "032x")
        record.otelServiceName = sys.argv[0]
        return record

    return record_factory


class LogLevelValueError(Exception):
    """
    Custom exception raise from velocitas_sdk package, when logger did not find\n
    the suitable value from among these [ERROR, DEBUG, INFO, WARNING, CRITICAL].
    """
