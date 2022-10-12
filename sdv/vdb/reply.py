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
        self.reply = reply

    def get(self, datapoint):
        datapoint_type = datapoint.__class__.__name__
        vdb_datapoint: BrokerDatapoint = self.reply.fields[datapoint.get_path()]
        datapoint_values = {
            "DataPointBoolean": vdb_datapoint.bool_value,
            "DataPointBooleanArray": list(vdb_datapoint.bool_array.values),
            "DataPointString": vdb_datapoint.string_value,
            "DataPointStringArray": list(vdb_datapoint.string_array.values),
            "DataPointDouble": vdb_datapoint.double_value,
            "DataPointDoubleArray": list(vdb_datapoint.double_array.values),
            "DataPointFloat": vdb_datapoint.float_value,
            "DataPointFloatArray": list(vdb_datapoint.float_array.values),
            "DataPointInt8": vdb_datapoint.int32_value,
            "DataPointInt8Array": list(vdb_datapoint.int32_array.values),
            "DataPointInt16": vdb_datapoint.int32_value,
            "DataPointInt16Array": list(vdb_datapoint.int32_array.values),
            "DataPointInt32": vdb_datapoint.int32_value,
            "DataPointInt32Array": list(vdb_datapoint.int32_array.values),
            "DataPointInt64": vdb_datapoint.int64_value,
            "DataPointInt64Array": list(vdb_datapoint.int64_array.values),
            "DataPointUint8": vdb_datapoint.uint32_value,
            "DataPointUint8Array": list(vdb_datapoint.uint32_array.values),
            "DataPointUint16": vdb_datapoint.uint32_value,
            "DataPointUint16Array": list(vdb_datapoint.uint32_array.values),
            "DataPointUint32": vdb_datapoint.uint32_value,
            "DataPointUint32Array": list(vdb_datapoint.uint32_array.values),
            "DataPointUint64": vdb_datapoint.uint64_value,
            "DataPointUint64Array": list(vdb_datapoint.uint64_array.values),
        }
        datapoint_value = datapoint_values.get(
            datapoint_type,
            Exception(f"Datapoint of type {datapoint_type} has an unknown value"),
        )

        if isinstance(datapoint_value, Exception):
            raise datapoint_value

        return datapoint_value
