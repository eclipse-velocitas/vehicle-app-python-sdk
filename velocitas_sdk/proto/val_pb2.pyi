from velocitas_sdk.proto import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetValueRequest(_message.Message):
    __slots__ = ("signal_id",)
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    signal_id: _types_pb2.SignalID
    def __init__(self, signal_id: _Optional[_Union[_types_pb2.SignalID, _Mapping]] = ...) -> None: ...

class GetValueResponse(_message.Message):
    __slots__ = ("data_point",)
    DATA_POINT_FIELD_NUMBER: _ClassVar[int]
    data_point: _types_pb2.Datapoint
    def __init__(self, data_point: _Optional[_Union[_types_pb2.Datapoint, _Mapping]] = ...) -> None: ...

class GetValuesRequest(_message.Message):
    __slots__ = ("signal_ids",)
    SIGNAL_IDS_FIELD_NUMBER: _ClassVar[int]
    signal_ids: _containers.RepeatedCompositeFieldContainer[_types_pb2.SignalID]
    def __init__(self, signal_ids: _Optional[_Iterable[_Union[_types_pb2.SignalID, _Mapping]]] = ...) -> None: ...

class GetValuesResponse(_message.Message):
    __slots__ = ("data_points",)
    DATA_POINTS_FIELD_NUMBER: _ClassVar[int]
    data_points: _containers.RepeatedCompositeFieldContainer[_types_pb2.Datapoint]
    def __init__(self, data_points: _Optional[_Iterable[_Union[_types_pb2.Datapoint, _Mapping]]] = ...) -> None: ...

class SubscribeRequest(_message.Message):
    __slots__ = ("signal_paths", "buffer_size", "filter")
    SIGNAL_PATHS_FIELD_NUMBER: _ClassVar[int]
    BUFFER_SIZE_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    signal_paths: _containers.RepeatedScalarFieldContainer[str]
    buffer_size: int
    filter: _types_pb2.Filter
    def __init__(self, signal_paths: _Optional[_Iterable[str]] = ..., buffer_size: _Optional[int] = ..., filter: _Optional[_Union[_types_pb2.Filter, _Mapping]] = ...) -> None: ...

class SubscribeResponse(_message.Message):
    __slots__ = ("entries",)
    class EntriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _types_pb2.Datapoint
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_types_pb2.Datapoint, _Mapping]] = ...) -> None: ...
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.MessageMap[str, _types_pb2.Datapoint]
    def __init__(self, entries: _Optional[_Mapping[str, _types_pb2.Datapoint]] = ...) -> None: ...

class SubscribeByIdRequest(_message.Message):
    __slots__ = ("signal_ids", "buffer_size", "filter")
    SIGNAL_IDS_FIELD_NUMBER: _ClassVar[int]
    BUFFER_SIZE_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    signal_ids: _containers.RepeatedScalarFieldContainer[int]
    buffer_size: int
    filter: _types_pb2.Filter
    def __init__(self, signal_ids: _Optional[_Iterable[int]] = ..., buffer_size: _Optional[int] = ..., filter: _Optional[_Union[_types_pb2.Filter, _Mapping]] = ...) -> None: ...

class SubscribeByIdResponse(_message.Message):
    __slots__ = ("entries",)
    class EntriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: _types_pb2.Datapoint
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[_types_pb2.Datapoint, _Mapping]] = ...) -> None: ...
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.MessageMap[int, _types_pb2.Datapoint]
    def __init__(self, entries: _Optional[_Mapping[int, _types_pb2.Datapoint]] = ...) -> None: ...

class ActuateRequest(_message.Message):
    __slots__ = ("signal_id", "value")
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    signal_id: _types_pb2.SignalID
    value: _types_pb2.Value
    def __init__(self, signal_id: _Optional[_Union[_types_pb2.SignalID, _Mapping]] = ..., value: _Optional[_Union[_types_pb2.Value, _Mapping]] = ...) -> None: ...

class ActuateResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class BatchActuateRequest(_message.Message):
    __slots__ = ("actuate_requests",)
    ACTUATE_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    actuate_requests: _containers.RepeatedCompositeFieldContainer[ActuateRequest]
    def __init__(self, actuate_requests: _Optional[_Iterable[_Union[ActuateRequest, _Mapping]]] = ...) -> None: ...

class BatchActuateResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListMetadataRequest(_message.Message):
    __slots__ = ("root", "filter")
    ROOT_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    root: str
    filter: str
    def __init__(self, root: _Optional[str] = ..., filter: _Optional[str] = ...) -> None: ...

class ListMetadataResponse(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.RepeatedCompositeFieldContainer[_types_pb2.Metadata]
    def __init__(self, metadata: _Optional[_Iterable[_Union[_types_pb2.Metadata, _Mapping]]] = ...) -> None: ...

class PublishValueRequest(_message.Message):
    __slots__ = ("signal_id", "data_point")
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_POINT_FIELD_NUMBER: _ClassVar[int]
    signal_id: _types_pb2.SignalID
    data_point: _types_pb2.Datapoint
    def __init__(self, signal_id: _Optional[_Union[_types_pb2.SignalID, _Mapping]] = ..., data_point: _Optional[_Union[_types_pb2.Datapoint, _Mapping]] = ...) -> None: ...

class PublishValueResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PublishValuesRequest(_message.Message):
    __slots__ = ("request_id", "data_points")
    class DataPointsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: _types_pb2.Datapoint
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[_types_pb2.Datapoint, _Mapping]] = ...) -> None: ...
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_POINTS_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    data_points: _containers.MessageMap[int, _types_pb2.Datapoint]
    def __init__(self, request_id: _Optional[int] = ..., data_points: _Optional[_Mapping[int, _types_pb2.Datapoint]] = ...) -> None: ...

class PublishValuesResponse(_message.Message):
    __slots__ = ("request_id", "status")
    class StatusEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: _types_pb2.Error
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[_types_pb2.Error, _Mapping]] = ...) -> None: ...
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    status: _containers.MessageMap[int, _types_pb2.Error]
    def __init__(self, request_id: _Optional[int] = ..., status: _Optional[_Mapping[int, _types_pb2.Error]] = ...) -> None: ...

class ProvideActuationRequest(_message.Message):
    __slots__ = ("actuator_identifiers",)
    ACTUATOR_IDENTIFIERS_FIELD_NUMBER: _ClassVar[int]
    actuator_identifiers: _containers.RepeatedCompositeFieldContainer[_types_pb2.SignalID]
    def __init__(self, actuator_identifiers: _Optional[_Iterable[_Union[_types_pb2.SignalID, _Mapping]]] = ...) -> None: ...

class ProvideActuationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ProvideSignalRequest(_message.Message):
    __slots__ = ("signals_sample_intervals",)
    class SignalsSampleIntervalsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: _types_pb2.SampleInterval
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[_types_pb2.SampleInterval, _Mapping]] = ...) -> None: ...
    SIGNALS_SAMPLE_INTERVALS_FIELD_NUMBER: _ClassVar[int]
    signals_sample_intervals: _containers.MessageMap[int, _types_pb2.SampleInterval]
    def __init__(self, signals_sample_intervals: _Optional[_Mapping[int, _types_pb2.SampleInterval]] = ...) -> None: ...

class ProvideSignalResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class BatchActuateStreamRequest(_message.Message):
    __slots__ = ("actuate_requests",)
    ACTUATE_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    actuate_requests: _containers.RepeatedCompositeFieldContainer[ActuateRequest]
    def __init__(self, actuate_requests: _Optional[_Iterable[_Union[ActuateRequest, _Mapping]]] = ...) -> None: ...

class BatchActuateStreamResponse(_message.Message):
    __slots__ = ("signal_id", "error")
    SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    signal_id: _types_pb2.SignalID
    error: _types_pb2.Error
    def __init__(self, signal_id: _Optional[_Union[_types_pb2.SignalID, _Mapping]] = ..., error: _Optional[_Union[_types_pb2.Error, _Mapping]] = ...) -> None: ...

class UpdateFilterRequest(_message.Message):
    __slots__ = ("request_id", "filters_update")
    class FiltersUpdateEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: _types_pb2.Filter
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[_types_pb2.Filter, _Mapping]] = ...) -> None: ...
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    FILTERS_UPDATE_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    filters_update: _containers.MessageMap[int, _types_pb2.Filter]
    def __init__(self, request_id: _Optional[int] = ..., filters_update: _Optional[_Mapping[int, _types_pb2.Filter]] = ...) -> None: ...

class UpdateFilterResponse(_message.Message):
    __slots__ = ("request_id", "filter_error")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    FILTER_ERROR_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    filter_error: _types_pb2.FilterError
    def __init__(self, request_id: _Optional[int] = ..., filter_error: _Optional[_Union[_types_pb2.FilterError, str]] = ...) -> None: ...

class ProviderErrorIndication(_message.Message):
    __slots__ = ("provider_error",)
    PROVIDER_ERROR_FIELD_NUMBER: _ClassVar[int]
    provider_error: _types_pb2.ProviderError
    def __init__(self, provider_error: _Optional[_Union[_types_pb2.ProviderError, str]] = ...) -> None: ...

class GetProviderValueRequest(_message.Message):
    __slots__ = ("request_id", "signal_ids")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_IDS_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    signal_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, request_id: _Optional[int] = ..., signal_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class GetProviderValueResponse(_message.Message):
    __slots__ = ("request_id", "entries")
    class EntriesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: _types_pb2.Datapoint
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[_types_pb2.Datapoint, _Mapping]] = ...) -> None: ...
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    entries: _containers.MessageMap[int, _types_pb2.Datapoint]
    def __init__(self, request_id: _Optional[int] = ..., entries: _Optional[_Mapping[int, _types_pb2.Datapoint]] = ...) -> None: ...

class OpenProviderStreamRequest(_message.Message):
    __slots__ = ("provide_actuation_request", "publish_values_request", "batch_actuate_stream_response", "provide_signal_request", "update_filter_response", "get_provider_value_response", "provider_error_indication")
    PROVIDE_ACTUATION_REQUEST_FIELD_NUMBER: _ClassVar[int]
    PUBLISH_VALUES_REQUEST_FIELD_NUMBER: _ClassVar[int]
    BATCH_ACTUATE_STREAM_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    PROVIDE_SIGNAL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FILTER_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GET_PROVIDER_VALUE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ERROR_INDICATION_FIELD_NUMBER: _ClassVar[int]
    provide_actuation_request: ProvideActuationRequest
    publish_values_request: PublishValuesRequest
    batch_actuate_stream_response: BatchActuateStreamResponse
    provide_signal_request: ProvideSignalRequest
    update_filter_response: UpdateFilterResponse
    get_provider_value_response: GetProviderValueResponse
    provider_error_indication: ProviderErrorIndication
    def __init__(self, provide_actuation_request: _Optional[_Union[ProvideActuationRequest, _Mapping]] = ..., publish_values_request: _Optional[_Union[PublishValuesRequest, _Mapping]] = ..., batch_actuate_stream_response: _Optional[_Union[BatchActuateStreamResponse, _Mapping]] = ..., provide_signal_request: _Optional[_Union[ProvideSignalRequest, _Mapping]] = ..., update_filter_response: _Optional[_Union[UpdateFilterResponse, _Mapping]] = ..., get_provider_value_response: _Optional[_Union[GetProviderValueResponse, _Mapping]] = ..., provider_error_indication: _Optional[_Union[ProviderErrorIndication, _Mapping]] = ...) -> None: ...

class OpenProviderStreamResponse(_message.Message):
    __slots__ = ("provide_actuation_response", "publish_values_response", "batch_actuate_stream_request", "provide_signal_response", "update_filter_request", "get_provider_value_request")
    PROVIDE_ACTUATION_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    PUBLISH_VALUES_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    BATCH_ACTUATE_STREAM_REQUEST_FIELD_NUMBER: _ClassVar[int]
    PROVIDE_SIGNAL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FILTER_REQUEST_FIELD_NUMBER: _ClassVar[int]
    GET_PROVIDER_VALUE_REQUEST_FIELD_NUMBER: _ClassVar[int]
    provide_actuation_response: ProvideActuationResponse
    publish_values_response: PublishValuesResponse
    batch_actuate_stream_request: BatchActuateStreamRequest
    provide_signal_response: ProvideSignalResponse
    update_filter_request: UpdateFilterRequest
    get_provider_value_request: GetProviderValueRequest
    def __init__(self, provide_actuation_response: _Optional[_Union[ProvideActuationResponse, _Mapping]] = ..., publish_values_response: _Optional[_Union[PublishValuesResponse, _Mapping]] = ..., batch_actuate_stream_request: _Optional[_Union[BatchActuateStreamRequest, _Mapping]] = ..., provide_signal_response: _Optional[_Union[ProvideSignalResponse, _Mapping]] = ..., update_filter_request: _Optional[_Union[UpdateFilterRequest, _Mapping]] = ..., get_provider_value_request: _Optional[_Union[GetProviderValueRequest, _Mapping]] = ...) -> None: ...

class GetServerInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetServerInfoResponse(_message.Message):
    __slots__ = ("name", "version", "commit_hash")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    COMMIT_HASH_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    commit_hash: str
    def __init__(self, name: _Optional[str] = ..., version: _Optional[str] = ..., commit_hash: _Optional[str] = ...) -> None: ...
