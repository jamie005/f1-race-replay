from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class F1CarTelemetryReport(_message.Message):
    __slots__ = ("driver", "latitude", "longitude", "speed_kmh", "engine_rpm", "gear", "throttle_percent", "brake_on", "on_track")
    DRIVER_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    SPEED_KMH_FIELD_NUMBER: _ClassVar[int]
    ENGINE_RPM_FIELD_NUMBER: _ClassVar[int]
    GEAR_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    BRAKE_ON_FIELD_NUMBER: _ClassVar[int]
    ON_TRACK_FIELD_NUMBER: _ClassVar[int]
    driver: str
    latitude: float
    longitude: float
    speed_kmh: float
    engine_rpm: float
    gear: int
    throttle_percent: int
    brake_on: bool
    on_track: bool
    def __init__(self, driver: _Optional[str] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., speed_kmh: _Optional[float] = ..., engine_rpm: _Optional[float] = ..., gear: _Optional[int] = ..., throttle_percent: _Optional[int] = ..., brake_on: bool = ..., on_track: bool = ...) -> None: ...
