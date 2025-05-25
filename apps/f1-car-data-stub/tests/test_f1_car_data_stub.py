import pandas as pd
import pytest
from fastf1.core import Telemetry
from google.protobuf.message import DecodeError
from kafka import KafkaProducer

from f1_car_data_stub import F1CarDataStub
from f1_car_data_stub.transformers.telemetry_transformer import TelemetryTransformer
from f1_replay_data_model_py.F1CarTelemetryReport_pb2 import F1CarTelemetryReport


@pytest.fixture
def telemetry(sample_telemetry_row: pd.Series) -> Telemetry:
    telemetry = pd.concat([sample_telemetry_row.to_frame().T], ignore_index=True)
    return telemetry


@pytest.fixture
def mock_kafka_producer(mocker) -> KafkaProducer:
    return mocker.Mock()


@pytest.fixture
def kafka_topic() -> str:
    return "mock-kafka-topic"


def test_f1_car_data_stub_sends_f1_telemetry_report_to_correct_topic(mock_kafka_producer: KafkaProducer,
                                                                     telemetry: Telemetry,
                                                                     telemetry_transformer: TelemetryTransformer,
                                                                     kafka_topic: str):
    serialised_f1_telemetry_report = telemetry_transformer.transform(telemetry.iloc[0]).SerializeToString()
    stub = F1CarDataStub(mock_kafka_producer, telemetry, telemetry_transformer, kafka_topic)

    stub.start()

    mock_kafka_producer.send.assert_called_once_with(kafka_topic, serialised_f1_telemetry_report)


def test_f1_car_data_stub_sends_message_for_each_row(mock_kafka_producer: KafkaProducer,
                                                     telemetry: Telemetry,
                                                     telemetry_transformer: TelemetryTransformer,
                                                     kafka_topic: str):
    multi_telemetry = pd.concat([telemetry, telemetry], ignore_index=True)
    stub = F1CarDataStub(mock_kafka_producer, multi_telemetry, telemetry_transformer, kafka_topic)

    stub.start()

    assert mock_kafka_producer.send.call_count == len(multi_telemetry)


def test_f1_car_data_stub_handles_kafka_send_exception(mock_kafka_producer: KafkaProducer, telemetry: Telemetry,
                                                       telemetry_transformer: TelemetryTransformer,
                                                       kafka_topic: str, caplog):
    mock_kafka_producer.send.side_effect = Exception("Kafka error")
    stub = F1CarDataStub(mock_kafka_producer, telemetry, telemetry_transformer, kafka_topic)

    with caplog.at_level("ERROR"):
        stub.start()

    assert "Failed to send telemetry to Kafka" in caplog.text


def test_f1_car_data_stub_serializes_telemetry_correctly(mock_kafka_producer: KafkaProducer, telemetry: Telemetry,
                                                         telemetry_transformer: TelemetryTransformer, kafka_topic: str):
    stub = F1CarDataStub(mock_kafka_producer, telemetry, telemetry_transformer, kafka_topic)

    stub.start()

    args, _ = mock_kafka_producer.send.call_args
    try:
        F1CarTelemetryReport().ParseFromString(args[1])
    except DecodeError:
        pytest.fail("Failed to decode F1CarTelemetryReport from Kafka message")


def test_f1_car_data_stub_with_empty_telemetry(mock_kafka_producer, telemetry_transformer, kafka_topic):
    empty_telemetry = Telemetry()
    stub = F1CarDataStub(mock_kafka_producer, empty_telemetry, telemetry_transformer, kafka_topic)

    stub.start()
    
    mock_kafka_producer.send.assert_not_called()
