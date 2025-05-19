from pydantic_settings import BaseSettings
from pydantic import KafkaDsn, field_validator

from f1_car_data_stub.geometry.track_origins import TRACK_WGS84_ORIGINS


class F1CarDataStubSettings(BaseSettings):
    """
    Settings for the F1 Car Data Stub application.

    Attributes:
        kafka_address (KafkaDsn): The Kafka broker address (default: "kafka://localhost:9094").
        log_level (str): The logging level (default: "INFO").
        driver (str): The driver's car to get telemetry from (default: "VER").
    """
    kafka_address: KafkaDsn = "kafka://localhost:9094"
    log_level: str = "INFO"
    driver: str = "VER"
    track: str = "Monza"

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"}
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}, got '{v}'")
        return v.upper()
    
    @field_validator("track")
    @classmethod
    def validate_track(cls, v: str) -> str:
        if v not in TRACK_WGS84_ORIGINS.keys():
            raise ValueError(f"'{v}' is not one of these supported tracks: {list(TRACK_WGS84_ORIGINS.keys())}")
        return v
