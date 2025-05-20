import logging
import time

import pandas as pd
from kafka import KafkaProducer
from fastf1.core import Telemetry

from f1_car_data_stub.transformers.telemetry_transformer import TelemetryTransformer


class F1CarDataStub:
    """
    Streams car telemetry data to a Kafka topic.

    This class takes telemetry data, transforms it into the appropriate protobuf message,
    and publishes it to a specified Kafka topic at intervals matching the telemetry timestamps.

    Args:
        producer (KafkaProducer): The Kafka producer instance used to send messages.
        car_telemetry (Telemetry): The telemetry data to be streamed.
        transformer (TelemetryTransformer): Transformer to convert telemetry rows to protobuf messages.
        topic (str): The Kafka topic to which telemetry messages will be sent.

    Attributes:
        _producer (KafkaProducer): Kafka producer for sending messages.
        _transformer (TelemetryTransformer): Transforms telemetry rows to protobuf messages.
        _car_telemetry (Telemetry): Telemetry data to stream.
        _topic (str): Kafka topic for telemetry messages.
        _logger (logging.Logger): Logger for this class.
    """

    def __init__(self, producer: KafkaProducer, car_telemetry: Telemetry,
                 transformer: TelemetryTransformer, topic: str) -> None:
        self._producer = producer
        self._transformer = transformer
        self._car_telemetry = car_telemetry
        self._topic = topic
        self._logger = logging.getLogger(__package__)

    def start(self) -> None:
        """
        Starts streaming telemetry data to Kafka.

        Iterates over the telemetry data, transforms each row, and sends it to the Kafka topic.
        The method respects the time intervals between telemetry samples to simulate real-time streaming.
        """
        previous_time = 0.0
        message_interval = 0.0
        for index, telemetry_row in self._car_telemetry.iterrows():
            time.sleep(message_interval)

            f1_car_telemetry_report = self._transformer.transform(telemetry_row)
            try:
                self._producer.send(self._topic, f1_car_telemetry_report.SerializeToString())
                self._logger.debug(f"Telemetry report {index} sent to kafka:\n{f1_car_telemetry_report}")
            except Exception as e:
                self._logger.error(f"Failed to send telemetry to Kafka: {e}")
            
            time_delta: pd.Timedelta = telemetry_row["Time"]
            message_interval = time_delta.total_seconds() - previous_time
            previous_time = time_delta.total_seconds()
