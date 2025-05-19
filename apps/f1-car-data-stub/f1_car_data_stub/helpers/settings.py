from pydantic_settings import BaseSettings
from pydantic import KafkaDsn, field_validator


class F1CarDataStubSettings(BaseSettings):
    kafka_address: KafkaDsn = "kafka://localhost:9094"
    log_level: str = "INFO"
    driver: str = "VER"

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"}
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}, got '{v}'")
        return v.upper()
