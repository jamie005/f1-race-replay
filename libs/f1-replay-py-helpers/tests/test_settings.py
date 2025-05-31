import pytest
from pydantic import ValidationError

from f1_replay_py_helpers.settings import BaseServiceSettings, BaseKafkaServiceSettings


def test_base_service_settings_defaults():
    settings = BaseServiceSettings()
    assert settings.log_level == "INFO"


def test_base_service_settings_valid_log_levels():
    for level in ["info", "DEBUG", "warning", "Error", "CRITICAL", "notset"]:
        settings = BaseServiceSettings(log_level=level)
        assert settings.log_level == level.upper()


def test_base_service_settings_invalid_log_level():
    with pytest.raises(ValidationError) as excinfo:
        BaseServiceSettings(log_level="INVALID")
    assert "log_level must be one of" in str(excinfo.value)


def test_base_kafka_service_settings_defaults():
    settings = BaseKafkaServiceSettings()
    assert settings.log_level == "INFO"
    assert settings.kafka_address == "localhost:9094"


def test_base_kafka_service_settings_override():
    settings = BaseKafkaServiceSettings(log_level="debug", kafka_address="kafka:1234")
    assert settings.log_level == "DEBUG"
    assert settings.kafka_address == "kafka:1234"
