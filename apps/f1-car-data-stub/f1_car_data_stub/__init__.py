import time
import pandas as pd

from f1_car_data_stub.transformers.telemetry_transformer import TelemetryTransformer
from f1_car_data_stub.geometry.wgs84_position import Wgs84Position
import fastf1
from kafka import KafkaProducer


class F1CarDataStub:
    def __init__(self):
        self._producer = KafkaProducer(bootstrap_servers='localhost:9094')
        self._transformer = TelemetryTransformer(Wgs84Position(45.617100, 9.282650))
        self._session = fastf1.get_session(2021, 'Monza', 'Race')

    def start(self):
        self._session.load()
        lap = self._session.laps.pick_drivers('VER').pick_laps(1)
        pos_data = lap.get_telemetry()
        previous_time = 0.0
        next_time_delta_seconds = 0.0
        for index, telemetry in pos_data.iterrows():
            time.sleep(next_time_delta_seconds)
            f1_car_telemetry_report = self._transformer.transform(telemetry)
            self._producer.send("bruh", f1_car_telemetry_report.SerializeToString())
            time_delta: pd.Timedelta = telemetry["Time"]
            next_time_delta_seconds = time_delta.total_seconds() - previous_time
            previous_time = time_delta.total_seconds()
            