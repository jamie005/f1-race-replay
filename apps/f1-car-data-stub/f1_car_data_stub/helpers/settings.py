from pydantic import field_validator

from f1_car_data_stub.geometry.track_origins import TRACK_WGS84_ORIGINS
from f1_replay_py_helpers.settings import BaseKafkaServiceSettings


class F1CarDataStubSettings(BaseKafkaServiceSettings):
    driver: str = "VER"
    track: str = "Monza"

    @field_validator("track")
    @classmethod
    def validate_track(cls, v: str) -> str:
        if v not in TRACK_WGS84_ORIGINS.keys():
            raise ValueError(f"'{v}' is not one of these supported tracks: {list(TRACK_WGS84_ORIGINS.keys())}")
        return v
