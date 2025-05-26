from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseF1RaceReplayServiceSettings(BaseSettings):
    log_level: str

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid_levels = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"}
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}, got '{v}'")
        return v.upper()
    
    model_config = SettingsConfigDict(env_file=".env")

class BaseKafkaServiceSettings(BaseF1RaceReplayServiceSettings):
    kafka_address: str
