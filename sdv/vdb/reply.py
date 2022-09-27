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

# pylint: skip-file
# flake8: noqa

from sdv.proto.types_pb2 import Datapoint as BrokerDatapoint


class DataPointReply:
    def __init__(self, reply):
        self._reply = reply

    def get(self, datapoint_object):
        datapoint_type = datapoint_object.__class__.__name__
        datapoint: BrokerDatapoint = self._reply.fields[datapoint_object.get_path()]
        try:
            if datapoint_type == "DataPointBoolean":
                return datapoint.bool_value
            elif datapoint_type == "DataPointBooleanArray":
                return list(datapoint.bool_array.values)
            elif datapoint_type == "DataPointString":
                return datapoint.string_value
            elif datapoint_type == "DataPointStringArray":
                return list(datapoint.string_array.values)
            elif datapoint_type == "DataPointDouble":
                return datapoint.double_value
            elif datapoint_type == "DataPointDoubleArray":
                return list(datapoint.double_array.values)
            elif datapoint_type == "DataPointFloat":
                return datapoint.float_value
            elif datapoint_type == "DataPointFloatArray":
                return list(datapoint.float_array.values)
            elif datapoint_type == "DataPointInt8":
                return datapoint.int32_value
            elif datapoint_type == "DataPointInt8Array":
                return list(datapoint.int32_array.values)
            elif datapoint_type == "DataPointInt16":
                return datapoint.int32_value
            elif datapoint_type == "DataPointInt16Array":
                return list(datapoint.int32_array.values)
            elif datapoint_type == "DataPointInt32":
                return datapoint.int32_value
            elif datapoint_type == "DataPointInt32Array":
                return list(datapoint.int32_array.values)
            elif datapoint_type == "DataPointInt64":
                return datapoint.int64_value
            elif datapoint_type == "DataPointInt64Array":
                return list(datapoint.int64_array.values)
            elif datapoint_type == "DataPointUint8":
                return datapoint.uint32_value
            elif datapoint_type == "DataPointUint8Array":
                return list(datapoint.uint32_array.values)
            elif datapoint_type == "DataPointUint16":
                return datapoint.uint32_value
            elif datapoint_type == "DataPointUint16Array":
                return list(datapoint.uint32_array.values)
            elif datapoint_type == "DataPointUint32":
                return datapoint.uint32_value
            elif datapoint_type == "DataPointUint32Array":
                return list(datapoint.uint32_array.values)
            elif datapoint_type == "DataPointUint64":
                return datapoint.uint64_value
            elif datapoint_type == "DataPointUint64Array":
                return list(datapoint.uint64_array.values)

        except Exception:
            raise
