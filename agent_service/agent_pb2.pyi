from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExperimentState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STATE_UNSPECIFIED: _ClassVar[ExperimentState]
    STATE_DEFINED: _ClassVar[ExperimentState]
    STATE_RUNNING: _ClassVar[ExperimentState]
    STATE_PAUSED: _ClassVar[ExperimentState]
    STATE_COMPLETED: _ClassVar[ExperimentState]
    STATE_FAILED: _ClassVar[ExperimentState]
    STATE_STOPPED: _ClassVar[ExperimentState]

class ExperimentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TYPE_UNSPECIFIED: _ClassVar[ExperimentType]
    FREELANCE_WRITING: _ClassVar[ExperimentType]
    NICHE_AFFILIATE_WEBSITE: _ClassVar[ExperimentType]
    AI_DRIVEN_EBOOKS: _ClassVar[ExperimentType]
    PINTEREST_STRATEGY: _ClassVar[ExperimentType]

class LogLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOG_LEVEL_UNSPECIFIED: _ClassVar[LogLevel]
    DEBUG: _ClassVar[LogLevel]
    INFO: _ClassVar[LogLevel]
    WARN: _ClassVar[LogLevel]
    ERROR: _ClassVar[LogLevel]
    CRITICAL: _ClassVar[LogLevel]
STATE_UNSPECIFIED: ExperimentState
STATE_DEFINED: ExperimentState
STATE_RUNNING: ExperimentState
STATE_PAUSED: ExperimentState
STATE_COMPLETED: ExperimentState
STATE_FAILED: ExperimentState
STATE_STOPPED: ExperimentState
TYPE_UNSPECIFIED: ExperimentType
FREELANCE_WRITING: ExperimentType
NICHE_AFFILIATE_WEBSITE: ExperimentType
AI_DRIVEN_EBOOKS: ExperimentType
PINTEREST_STRATEGY: ExperimentType
LOG_LEVEL_UNSPECIFIED: LogLevel
DEBUG: LogLevel
INFO: LogLevel
WARN: LogLevel
ERROR: LogLevel
CRITICAL: LogLevel

class ExperimentDefinition(_message.Message):
    __slots__ = ("type", "name", "description", "parameters")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    type: ExperimentType
    name: str
    description: str
    parameters: _struct_pb2.Struct
    def __init__(self, type: _Optional[_Union[ExperimentType, str]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., parameters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class ExperimentId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DecisionId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class StatusResponse(_message.Message):
    __slots__ = ("success", "message", "error_code")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    error_code: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., error_code: _Optional[str] = ...) -> None: ...

class AgentStatus(_message.Message):
    __slots__ = ("agent_state", "active_experiments", "cpu_usage_percent", "memory_usage_mb", "last_updated")
    AGENT_STATE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_EXPERIMENTS_FIELD_NUMBER: _ClassVar[int]
    CPU_USAGE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_USAGE_MB_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    agent_state: str
    active_experiments: int
    cpu_usage_percent: float
    memory_usage_mb: float
    last_updated: _timestamp_pb2.Timestamp
    def __init__(self, agent_state: _Optional[str] = ..., active_experiments: _Optional[int] = ..., cpu_usage_percent: _Optional[float] = ..., memory_usage_mb: _Optional[float] = ..., last_updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ExperimentStatus(_message.Message):
    __slots__ = ("id", "name", "type", "state", "status_message", "metrics", "start_time", "last_update_time", "estimated_completion_time")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_COMPLETION_TIME_FIELD_NUMBER: _ClassVar[int]
    id: ExperimentId
    name: str
    type: ExperimentType
    state: ExperimentState
    status_message: str
    metrics: _struct_pb2.Struct
    start_time: _timestamp_pb2.Timestamp
    last_update_time: _timestamp_pb2.Timestamp
    estimated_completion_time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[_Union[ExperimentId, _Mapping]] = ..., name: _Optional[str] = ..., type: _Optional[_Union[ExperimentType, str]] = ..., state: _Optional[_Union[ExperimentState, str]] = ..., status_message: _Optional[str] = ..., metrics: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., estimated_completion_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class LogEntry(_message.Message):
    __slots__ = ("timestamp", "level", "message", "experiment_id", "source_component")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_COMPONENT_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    level: LogLevel
    message: str
    experiment_id: ExperimentId
    source_component: str
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., level: _Optional[_Union[LogLevel, str]] = ..., message: _Optional[str] = ..., experiment_id: _Optional[_Union[ExperimentId, _Mapping]] = ..., source_component: _Optional[str] = ...) -> None: ...

class CreateExperimentRequest(_message.Message):
    __slots__ = ("definition",)
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    definition: ExperimentDefinition
    def __init__(self, definition: _Optional[_Union[ExperimentDefinition, _Mapping]] = ...) -> None: ...

class CreateExperimentResponse(_message.Message):
    __slots__ = ("id", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: ExperimentId
    status: StatusResponse
    def __init__(self, id: _Optional[_Union[ExperimentId, _Mapping]] = ..., status: _Optional[_Union[StatusResponse, _Mapping]] = ...) -> None: ...

class StartExperimentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: ExperimentId
    def __init__(self, id: _Optional[_Union[ExperimentId, _Mapping]] = ...) -> None: ...

class StopExperimentRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: ExperimentId
    def __init__(self, id: _Optional[_Union[ExperimentId, _Mapping]] = ...) -> None: ...

class GetExperimentStatusRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: ExperimentId
    def __init__(self, id: _Optional[_Union[ExperimentId, _Mapping]] = ...) -> None: ...

class GetAgentStatusRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetLogsRequest(_message.Message):
    __slots__ = ("experiment_id", "minimum_level")
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_LEVEL_FIELD_NUMBER: _ClassVar[int]
    experiment_id: ExperimentId
    minimum_level: LogLevel
    def __init__(self, experiment_id: _Optional[_Union[ExperimentId, _Mapping]] = ..., minimum_level: _Optional[_Union[LogLevel, str]] = ...) -> None: ...

class ApproveDecisionRequest(_message.Message):
    __slots__ = ("decision_id", "user_id", "approved", "comment")
    DECISION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    APPROVED_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    decision_id: DecisionId
    user_id: str
    approved: bool
    comment: str
    def __init__(self, decision_id: _Optional[_Union[DecisionId, _Mapping]] = ..., user_id: _Optional[str] = ..., approved: bool = ..., comment: _Optional[str] = ...) -> None: ...

class StopAgentRequest(_message.Message):
    __slots__ = ("reason",)
    REASON_FIELD_NUMBER: _ClassVar[int]
    reason: str
    def __init__(self, reason: _Optional[str] = ...) -> None: ...
