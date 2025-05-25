import pandas as pd
import pymap3d
import pytest

from f1_car_data_stub.geometry.wgs84_position import Wgs84Position
from f1_car_data_stub.transformers.telemetry_transformer import TelemetryTransformer


def test_x_y_coordinates_are_transformed(telemetry_transformer: TelemetryTransformer,
                                         sample_telemetry_row: pd.Series, wgs84_origin: Wgs84Position):
    latitude, longitude, _ = pymap3d.enu2geodetic(sample_telemetry_row['X'] / 10,
                                                  sample_telemetry_row['Y'] /
                                                  10, 0,
                                                  wgs84_origin.latitude,
                                                  wgs84_origin.longitude,
                                                  wgs84_origin.altitude)

    f1_car_telemetry_report = telemetry_transformer.transform(sample_telemetry_row)
    assert f1_car_telemetry_report.latitude == latitude
    assert f1_car_telemetry_report.longitude == longitude


def test_rpm_speed_ngear_throttle_brake_telemetry_is_transformed(telemetry_transformer: TelemetryTransformer,
                                                                 sample_telemetry_row: pd.Series):
    f1_car_telemetry_report = telemetry_transformer.transform(sample_telemetry_row)
    assert f1_car_telemetry_report.engine_rpm == sample_telemetry_row["RPM"]
    assert f1_car_telemetry_report.speed_kmh == sample_telemetry_row["Speed"]
    assert f1_car_telemetry_report.gear == sample_telemetry_row["nGear"]
    assert f1_car_telemetry_report.throttle_percent == sample_telemetry_row["Throttle"]
    assert f1_car_telemetry_report.brake_on == sample_telemetry_row["Brake"]


def test_ontrack_status_is_transformed(telemetry_transformer: TelemetryTransformer,
                                       sample_telemetry_row: pd.Series):
    sample_telemetry_row["Status"] = "OnTrack"
    f1_car_telemetry_report = telemetry_transformer.transform(sample_telemetry_row)
    assert f1_car_telemetry_report.on_track is True


def test_offtrack_status_is_transformed(telemetry_transformer: TelemetryTransformer, sample_telemetry_row: pd.Series):
    sample_telemetry_row["Status"] = "OffTrack"
    f1_car_telemetry_report = telemetry_transformer.transform(sample_telemetry_row)
    assert f1_car_telemetry_report.on_track is False
