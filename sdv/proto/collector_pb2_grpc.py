# Copyright (c) 2022-2023 Robert Bosch GmbH and Microsoft Corporation
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

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from sdv.proto import collector_pb2 as sdv_dot_databroker_dot_v1_dot_collector__pb2


class CollectorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterDatapoints = channel.unary_unary(
                '/sdv.databroker.v1.Collector/RegisterDatapoints',
                request_serializer=sdv_dot_databroker_dot_v1_dot_collector__pb2.RegisterDatapointsRequest.SerializeToString,
                response_deserializer=sdv_dot_databroker_dot_v1_dot_collector__pb2.RegisterDatapointsReply.FromString,
                )
        self.UpdateDatapoints = channel.unary_unary(
                '/sdv.databroker.v1.Collector/UpdateDatapoints',
                request_serializer=sdv_dot_databroker_dot_v1_dot_collector__pb2.UpdateDatapointsRequest.SerializeToString,
                response_deserializer=sdv_dot_databroker_dot_v1_dot_collector__pb2.UpdateDatapointsReply.FromString,
                )
        self.StreamDatapoints = channel.stream_stream(
                '/sdv.databroker.v1.Collector/StreamDatapoints',
                request_serializer=sdv_dot_databroker_dot_v1_dot_collector__pb2.StreamDatapointsRequest.SerializeToString,
                response_deserializer=sdv_dot_databroker_dot_v1_dot_collector__pb2.StreamDatapointsReply.FromString,
                )


class CollectorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RegisterDatapoints(self, request, context):
        """Register new datapoint (metadata)

        If the registration of at least one of the passed data point fails, the overall registration
        is rejected and the gRPC status code ABORTED is returned (to indicate the "aborted" registration).
        The details, which data point(s) caused the failure and the reason, is passed in back in human-
        readable form in the status message. Possible failure resaons are:
        * PERMISSION_DENIED - Not allowed to register this name
        * ALREADY_REGISTERED - The data point is already registered by some other feeder
        * RE_REGISTRATION_MISMATCH - Already registered by this feeder but with differing metadata
        * INVALID_NAME - The passed name of the datapoint has an invalid structure
        * INVALID_VALUE_TYPE - The passed ValueType is not supported
        * INVALID_CHANGE_TYPE - The passed ChangeType is not supported
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDatapoints(self, request, context):
        """Provide a set of updated datapoint values to the broker.
        This is the unary equivalent of `StreamDatapoints` below and is better suited for cases
        where the frequency of updates is rather low.

        NOTE: The values provided in a single request are handled as a single update in the
        data broker. This ensures that any clients requesting (or subscribing to) a set of
        datapoints will get a consistent update, i.e. that either all values are updated or
        none are.

        Returns: any errors encountered updating the datapoints

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamDatapoints(self, request_iterator, context):
        """Provide a stream with updated datapoint values to the broker.
        This is the streaming equivalent of `UpdateDatapoints` above and is better suited for
        cases where the frequency of updates is high.

        NOTE: The values provided in a single request are handled as a single update in the
        data broker. This ensures that any clients requesting (or subscribing to) a set of
        datapoints will get a consistent update, i.e. that either all values are updated or
        none are.

        Returns: any errors encountered updating the datapoints

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CollectorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterDatapoints': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterDatapoints,
                    request_deserializer=sdv_dot_databroker_dot_v1_dot_collector__pb2.RegisterDatapointsRequest.FromString,
                    response_serializer=sdv_dot_databroker_dot_v1_dot_collector__pb2.RegisterDatapointsReply.SerializeToString,
            ),
            'UpdateDatapoints': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateDatapoints,
                    request_deserializer=sdv_dot_databroker_dot_v1_dot_collector__pb2.UpdateDatapointsRequest.FromString,
                    response_serializer=sdv_dot_databroker_dot_v1_dot_collector__pb2.UpdateDatapointsReply.SerializeToString,
            ),
            'StreamDatapoints': grpc.stream_stream_rpc_method_handler(
                    servicer.StreamDatapoints,
                    request_deserializer=sdv_dot_databroker_dot_v1_dot_collector__pb2.StreamDatapointsRequest.FromString,
                    response_serializer=sdv_dot_databroker_dot_v1_dot_collector__pb2.StreamDatapointsReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sdv.databroker.v1.Collector', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Collector(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RegisterDatapoints(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdv.databroker.v1.Collector/RegisterDatapoints',
            sdv_dot_databroker_dot_v1_dot_collector__pb2.RegisterDatapointsRequest.SerializeToString,
            sdv_dot_databroker_dot_v1_dot_collector__pb2.RegisterDatapointsReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateDatapoints(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdv.databroker.v1.Collector/UpdateDatapoints',
            sdv_dot_databroker_dot_v1_dot_collector__pb2.UpdateDatapointsRequest.SerializeToString,
            sdv_dot_databroker_dot_v1_dot_collector__pb2.UpdateDatapointsReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StreamDatapoints(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/sdv.databroker.v1.Collector/StreamDatapoints',
            sdv_dot_databroker_dot_v1_dot_collector__pb2.StreamDatapointsRequest.SerializeToString,
            sdv_dot_databroker_dot_v1_dot_collector__pb2.StreamDatapointsReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
