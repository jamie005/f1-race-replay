import pandas as pd
import pymap3d
import pytest

from f1_car_data_stub.geometry.wgs84_position import Wgs84Position
from f1_car_data_stub.geometry.track_origins import TRACK_WGS84_ORIGINS
from f1_car_data_stub.transformers.telemetry_transformer import TelemetryTransformer


@pytest.fixture
def wgs84_origin() -> Wgs84Position:
    return Wgs84Position(45.617100, 9.282650)


@pytest.fixture
def telemetry_transformer(wgs84_origin: Wgs84Position) -> TelemetryTransformer:
    return TelemetryTransformer(wgs84_origin)


@pytest.fixture
def sample_telemetry() -> pd.Series:
    return pd.Series({
        "X": 100.0,           # ENU X position (meters * 10)
        "Y": 200.0,           # ENU Y position (meters * 10)
        "RPM": 12000,         # Engine RPM
        "Speed": 320.5,       # Speed in km/h
        "nGear": 8,           # Gear number
        "Throttle": 98.5,     # Throttle percent
        "Brake": True,        # Brake on/off
        "Status": "OnTrack",  # Track status
        "Time": pd.Timedelta(seconds=10.0)  # Time as pd.Timedelta
    })


def test_x_y_coordinates_are_transformed(telemetry_transformer: TelemetryTransformer,
                                         sample_telemetry: pd.Series, wgs84_origin: Wgs84Position):
    latitude, longitude, _ = pymap3d.enu2geodetic(sample_telemetry['X'] / 10,
                                                  sample_telemetry['Y'] /
                                                  10, 0,
                                                  wgs84_origin.latitude,
                                                  wgs84_origin.longitude,
                                                  wgs84_origin.altitude)

    f1_car_telemetry_report = telemetry_transformer.transform(sample_telemetry)
    assert f1_car_telemetry_report.latitude == latitude
    assert f1_car_telemetry_report.longitude == longitude


def test_rpm_speed_ngear_throttle_brake_telemetry_is_transformed(telemetry_transformer: TelemetryTransformer,
                                                                 sample_telemetry: pd.Series):
    f1_car_telemetry_report = telemetry_transformer.transform(sample_telemetry)
    assert f1_car_telemetry_report.engine_rpm == sample_telemetry["RPM"]
    assert f1_car_telemetry_report.speed_kmh == sample_telemetry["Speed"]
    assert f1_car_telemetry_report.gear == sample_telemetry["nGear"]
    assert f1_car_telemetry_report.throttle_percent == sample_telemetry["Throttle"]
    assert f1_car_telemetry_report.brake_on == sample_telemetry["Brake"]


def test_ontrack_status_is_transformed(telemetry_transformer: TelemetryTransformer,
                                       sample_telemetry: pd.Series):
    sample_telemetry["Status"] = "OnTrack"
    f1_car_telemetry_report = telemetry_transformer.transform(sample_telemetry)
    assert f1_car_telemetry_report.on_track is True


def test_offtrack_status_is_transformed(telemetry_transformer: TelemetryTransformer, sample_telemetry: pd.Series):
    sample_telemetry["Status"] = "OffTrack"
    f1_car_telemetry_report = telemetry_transformer.transform(sample_telemetry)
    assert f1_car_telemetry_report.on_track is False
