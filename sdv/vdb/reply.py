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

from sdv.proto.types_pb2 import Datapoint as BrokerDatapoint


class DataPointReply:
    """Wrapper for dynamic datatype casting of VDB reply."""

    def __init__(self, reply):
        self._reply = reply

    def get(self, datapoint_object):
        datapoint_type = datapoint_object.__class__.__name__
        datapoint: BrokerDatapoint = self._reply.fields[datapoint_object.get_path()]
        datapoint_values = {
            "DataPointBoolean": datapoint.bool_value,
            "DataPointBooleanArray": list(datapoint.bool_array.values),
            "DataPointString": datapoint.string_value,
            "DataPointStringArray": list(datapoint.string_array.values),
            "DataPointDouble": datapoint.double_value,
            "DataPointDoubleArray": list(datapoint.double_array.values),
            "DataPointFloat": datapoint.float_value,
            "DataPointFloatArray": list(datapoint.float_array.values),
            "DataPointInt8": datapoint.int32_value,
            "DataPointInt8Array": list(datapoint.int32_array.values),
            "DataPointInt16": datapoint.int32_value,
            "DataPointInt16Array": list(datapoint.int32_array.values),
            "DataPointInt32": datapoint.int32_value,
            "DataPointInt32Array": list(datapoint.int32_array.values),
            "DataPointInt64": datapoint.int64_value,
            "DataPointInt64Array": list(datapoint.int64_array.values),
            "DataPointUint8": datapoint.uint32_value,
            "DataPointUint8Array": list(datapoint.uint32_array.values),
            "DataPointUint16": datapoint.uint32_value,
            "DataPointUint16Array": list(datapoint.uint32_array.values),
            "DataPointUint32": datapoint.uint32_value,
            "DataPointUint32Array": list(datapoint.uint32_array.values),
            "DataPointUint64": datapoint.uint64_value,
            "DataPointUint64Array": list(datapoint.uint64_array.values),
        }
        datapoint_value = datapoint_values.get(
            datapoint_type,
            Exception(f"Datapoint of type {datapoint_type} has an unknown value"),
        )

        if isinstance(datapoint_value, Exception):
            raise datapoint_value

        return datapoint_value
