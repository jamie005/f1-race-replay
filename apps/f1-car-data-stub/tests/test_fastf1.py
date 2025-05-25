import pytest

from fastf1.core import Telemetry

from f1_car_data_stub.helpers.fastf1 import get_car_telemetry


TRACK = "Monza"
YEAR = 2021
SESSION_TYPE = "Race"
DRIVER = "VER"


def test_valid_session_and_driver():
    car_telemetry = get_car_telemetry(TRACK, YEAR, SESSION_TYPE, DRIVER)
    assert car_telemetry is not None
    assert isinstance(car_telemetry, Telemetry)
    assert len(car_telemetry) > 0, "Telemetry data should not be empty"


@pytest.mark.parametrize(
    ("track", "year", "session_type", "driver", "match"),
    [
        (TRACK, YEAR, SESSION_TYPE, "BRUH", "no driver number!"),
        (TRACK, YEAR, "BRUH", DRIVER, "Invalid session type 'BRUH'"),
        (TRACK, 0, SESSION_TYPE, DRIVER, "Failed to load any schedule data."),
        (TRACK, 3000, SESSION_TYPE, DRIVER,
         "zero-size array to reduction operation maximum which has no identity"),
    ]
)
def test_invalid_inputs(track, year, session_type, driver, match):
    """Test that invalid inputs raise ValueError with expected message."""
    with pytest.raises(ValueError, match=match):
        get_car_telemetry(track, year, session_type, driver)
