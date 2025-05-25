import pandas as pd
import pytest

from f1_car_data_stub.geometry.wgs84_position import Wgs84Position
from f1_car_data_stub.transformers.telemetry_transformer import TelemetryTransformer


@pytest.fixture
def sample_telemetry_row() -> pd.Series:
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


@pytest.fixture
def wgs84_origin() -> Wgs84Position:
    return Wgs84Position(45.617100, 9.282650)


@pytest.fixture
def telemetry_transformer(wgs84_origin: Wgs84Position) -> TelemetryTransformer:
    return TelemetryTransformer(wgs84_origin)
