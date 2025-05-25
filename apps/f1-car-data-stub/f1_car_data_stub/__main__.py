import logging
import sys

from kafka import KafkaProducer

from f1_car_data_stub import F1CarDataStub
from f1_car_data_stub.geometry.track_origins import TRACK_WGS84_ORIGINS
from f1_car_data_stub.helpers.fastf1 import get_car_telemetry
from f1_car_data_stub.helpers.logging import color_log_handler
from f1_car_data_stub.helpers.settings import F1CarDataStubSettings
from f1_car_data_stub.transformers.telemetry_transformer import TelemetryTransformer


TRACK = "Monza"
YEAR = 2021
SESSION_TYPE = "Race"


def main() -> None:
    # Default WARNING level logger setup
    logger = logging.getLogger(__package__)
    logger.addHandler(color_log_handler)

    # Load settings
    try:
        settings = F1CarDataStubSettings()
    except ValueError as e:
        logger.error(f"Invalid settings: {e}")
        sys.exit(1)

    # Log level adjustment
    logger.setLevel(settings.log_level)

    # Kafka producer setup
    logger.info(f"Connecting to Kafka at {settings.kafka_address.encoded_string()}...")
    try:
        kafka_producer = KafkaProducer(bootstrap_servers=settings.kafka_address.encoded_string())
    except Exception as e:
        logger.error(f"Failed to create Kafka producer: {e}")
        sys.exit(1)
    logger.info("Kafka producer created successfully!")

    # Load car telemetry
    logger.info(f"Loading {settings.driver}'s {TRACK} {YEAR} {SESSION_TYPE} car telemetry...")
    try:
        car_telemetry = get_car_telemetry(TRACK, YEAR, SESSION_TYPE, settings.driver)
    except Exception as e:
        logger.error(f"Failed to load car telemetry: {e}")
        sys.exit(1)
    logger.info("Car telemetry loaded successfully!")

    telemetry_transformer = TelemetryTransformer(TRACK_WGS84_ORIGINS[settings.track])
    publish_topic = f"f1-race-replay.telemetry.{settings.driver.lower()}"

    # Start F1 Car Data Stub
    stub = F1CarDataStub(kafka_producer, car_telemetry, telemetry_transformer, publish_topic)
    logger.info("Starting F1 Car Data Stub...")
    try:
        stub.start()
    except KeyboardInterrupt:
        logger.info("Shutting down F1 Car Data Stub...")

    logger.info("Finished sending telemetry!")


if __name__ == "__main__":
    main()
