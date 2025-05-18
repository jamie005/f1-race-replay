import logging
import sys

import fastf1
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from f1_car_data_stub import F1CarDataStub
from f1_car_data_stub.helpers.logging import configure_logger


def main():
    # Logger setup
    logger = logging.getLogger(__package__)
    configure_logger(logger, "INFO")

    # Kafka setup
    logger.info("Creating Kafka producer...")
    try:
        kafka_producer = KafkaProducer(bootstrap_servers="localhost:9094", value_serializer=lambda v: v.SerializeToString())
    except NoBrokersAvailable:
        logger.critical(f"Kafka broker not available. Please start the Kafka broker.")
        sys.exit(1)
    logger.info("Kafka producer created!")

    # FastF1 setup
    fastf1.set_log_level(logging.CRITICAL) # Set to CRITICAL to avoid FastF1 logs
    try:
        session = fastf1.get_session(2021, 'Monza', 'Race')
        session.load(weather=False, messages=False)
    except Exception as e:
        logger.critical(f"Failed to load FastF1 session: {e}")
        sys.exit(1)
    driver_laps = session.laps.pick_drivers('VER')
    car_telemetry = driver_laps.get_telemetry()

    # F1CarDataStub setup
    stub = F1CarDataStub(kafka_producer, car_telemetry)
    stub.start()

if __name__ == "__main__":
    main()
