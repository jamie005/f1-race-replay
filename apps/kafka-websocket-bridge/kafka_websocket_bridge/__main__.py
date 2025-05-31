import asyncio
import functools
import logging

from f1_replay_py_helpers.logging import color_log_handler
from kafka_websocket_bridge import (
    create_kafka_consumer,
    start_kafka_websocket_bridge,
    kafka_websocket_handler
)
from kafka_websocket_bridge.settings import KafkaWebsocketBridgeSettings


async def main(logger: logging.Logger) -> None:
    # Logger and settings setup
    logger.addHandler(color_log_handler)
    try:
        settings = KafkaWebsocketBridgeSettings()
    except ValueError as e:
        logger.error(f"Invalid settings: {e}")
        return
    logger.setLevel(settings.log_level)

    # Setting up the kafka websocket bridge
    consumer = create_kafka_consumer(settings.kafka_address, settings.kafka_topic_pattern)
    handler = functools.partial(kafka_websocket_handler, consumer=consumer)
    try:
        logger.info(f"Connecting to Kafka at {settings.kafka_address} with topic pattern: ",
                    f"{settings.kafka_topic_pattern}...")
        await consumer.start()
        logger.info("Kafka consumer connected successfully!")

        logger.info(f"Starting WebSocket server at {settings.websocket_host}:{settings.websocket_port}...")
        await start_kafka_websocket_bridge(handler, settings.websocket_host, settings.websocket_port)
    except Exception as e:
        logger.error(f"Error in Kafka Websocket Bridge: {e}")
    finally:
        logger.info("Shutting down Kafka consumer...")
        await consumer.stop()


if __name__ == "__main__":
    logger = logging.getLogger(__package__)
    try:
        asyncio.run(main(logger))
    except KeyboardInterrupt:
        logger.info("Ctrl+C received, shutting down...")
