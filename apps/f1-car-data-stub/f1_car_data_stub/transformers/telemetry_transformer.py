import logging

import pandas as pd
import pymap3d

from f1_car_data_stub.geometry.wgs84_position import Wgs84Position
from f1_replay_data_model_py.F1CarTelemetryReport_pb2 import F1CarTelemetryReport


class TelemetryTransformer():
    """
    Transforms raw telemetry data into F1CarTelemetryReport protobuf messages.

    This class converts telemetry data from a pandas Series, including ENU (East-North-Up)
    coordinates, into geodetic coordinates (latitude, longitude) using a specified WGS84 origin.
    It also maps other telemetry fields to the corresponding fields in the F1CarTelemetryReport.

    Attributes:
        _origin (Wgs84Position): The WGS84 origin used for coordinate transformation.
        _logger (logging.Logger): Logger for the transformer.
    """

    def __init__(self, driver: str, origin: Wgs84Position) -> None:
        """
        Initialize the TelemetryTransformer.

        Args:
            origin (Wgs84Position): The WGS84 origin for ENU to geodetic conversion.
        """
        self._driver: str = driver
        self._origin: Wgs84Position = origin
        self._logger = logging.getLogger(__package__)

    def transform(self, telemetry: pd.Series) -> F1CarTelemetryReport:
        """
        Transform a telemetry pandas Series into a F1CarTelemetryReport protobuf message.

        Args:
            telemetry (pd.Series): The telemetry data for a single time step.

        Returns:
            F1CarTelemetryReport: The populated telemetry report message.
        """
        latitude, longitude, _ = pymap3d.enu2geodetic(telemetry['X'] / 10,
                                                      telemetry['Y'] / 10, 0,
                                                      self._origin.latitude,
                                                      self._origin.longitude,
                                                      self._origin.altitude)
        f1_car_telemetry_report = F1CarTelemetryReport()
        f1_car_telemetry_report.driver = self._driver
        f1_car_telemetry_report.latitude = latitude
        f1_car_telemetry_report.longitude = longitude

        # TODO Create separate transformer for car performance data
        # f1_car_telemetry_report.engine_rpm = telemetry["RPM"]
        # f1_car_telemetry_report.speed_kmh = telemetry["Speed"]
        # f1_car_telemetry_report.gear = telemetry["nGear"]
        # f1_car_telemetry_report.throttle_percent = telemetry["Throttle"]
        # f1_car_telemetry_report.brake_on = telemetry["Brake"]

        if telemetry["Status"] == "OnTrack":
            f1_car_telemetry_report.on_track = True
        elif telemetry["Status"] == "OffTrack":
            f1_car_telemetry_report.on_track = False
        else:
            self._logger.warning(f"Unknown telemetry status: {telemetry['Status']}")

        return f1_car_telemetry_report
