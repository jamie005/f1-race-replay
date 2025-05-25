import pytest

from fastf1.core import Telemetry

from f1_car_data_stub.helpers.fastf1 import get_car_telemetry


def test_valid_session_and_driver():
    car_telemetry = get_car_telemetry("Monza", 2021, "Race", "VER")
    assert car_telemetry is not None
    assert isinstance(car_telemetry, Telemetry)
    assert len(car_telemetry) > 0, "Telemetry data should not be empty"


def test_invalid_driver():
    with pytest.raises(ValueError, match="Cannot slice telemetry because self contains no driver number!"):
        get_car_telemetry("Monza", 2021, "Race", "BRUH")


def test_invalid_session_type():
    with pytest.raises(ValueError, match="Invalid session type 'BRUH'"):
        get_car_telemetry("Monza", 2021, "BRUH", "VER")


def test_invalid_year():
    with pytest.raises(ValueError, match="Failed to load any schedule data."):
        get_car_telemetry("Monza", 0, "Race", "VER")

def test_future_year():
    with pytest.raises(ValueError, match="zero-size array to reduction operation maximum which has no identity"):
        get_car_telemetry("Monza", 3000, "Race", "VER")
