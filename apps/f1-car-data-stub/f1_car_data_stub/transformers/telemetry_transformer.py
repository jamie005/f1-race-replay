from f1_car_data_stub.geometry.wgs84_position import Wgs84Position
import pandas as pd

from f1_replay_data_model_py.F1CarTelemetryReport_pb2 import F1CarTelemeteryReport
import pymap3d


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
        return f1_car_telemetry_report
