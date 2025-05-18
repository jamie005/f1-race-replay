import pandas as pd
import pymap3d

from f1_replay_data_model_py.F1CarTelemetryReport_pb2 import F1CarTelemeteryReport
from f1_car_data_stub.geometry.wgs84_position import Wgs84Position


class TelemetryTransformer():
    def __init__(self, origin: Wgs84Position) -> None:
        self._origin: Wgs84Position = origin

    def transform(self, telemetry: pd.Series) -> F1CarTelemeteryReport:
        latitude, longitude, _ = pymap3d.enu2geodetic(telemetry['X'] / 10,
                                                      telemetry['Y'] / 10, 0,
                                                      self._origin.latitude,
                                                      self._origin.longitude,
                                                      self._origin.altitude)
        f1_car_telemetry_report = F1CarTelemeteryReport()
        f1_car_telemetry_report.latitude = latitude
        f1_car_telemetry_report.longitude = longitude
        f1_car_telemetry_report.engine_rpm = telemetry["RPM"]
        f1_car_telemetry_report.speed_kmh = telemetry["Speed"]
        f1_car_telemetry_report.gear = telemetry["nGear"]
        f1_car_telemetry_report.engine_rpm = telemetry["Throttle"]
        f1_car_telemetry_report.brake_on = telemetry["Brake"]

        if telemetry["Status"] == "OnTrack":
            f1_car_telemetry_report.on_track = True
        elif telemetry["Status"] == "OffTrack":
            f1_car_telemetry_report.on_track = False

        return f1_car_telemetry_report
