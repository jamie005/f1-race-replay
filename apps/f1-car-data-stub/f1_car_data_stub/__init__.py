import logging
import time
import pandas as pd

from f1_car_data_stub.transformers.telemetry_transformer import TelemetryTransformer
from f1_car_data_stub.geometry.wgs84_position import Wgs84Position

from kafka import KafkaProducer
from fastf1.core import Telemetry


class F1CarDataStub:
    def __init__(self, producer: KafkaProducer, car_telemetry: Telemetry):
        self._producer = producer
        self._transformer = TelemetryTransformer(Wgs84Position(45.617100, 9.282650))
        self._car_telemetry = car_telemetry
        self._logger = logging.getLogger(__package__)

    def start(self):
        previous_time = 0.0
        next_time_delta_seconds = 0.0
        for _, telemetry in self._car_telemetry.iterrows():
            time.sleep(next_time_delta_seconds)
            f1_car_telemetry_report = self._transformer.transform(telemetry)
            self._producer.send("bruh", f1_car_telemetry_report)
            time_delta: pd.Timedelta = telemetry["Time"]
            next_time_delta_seconds = time_delta.total_seconds() - previous_time
            previous_time = time_delta.total_seconds()
            