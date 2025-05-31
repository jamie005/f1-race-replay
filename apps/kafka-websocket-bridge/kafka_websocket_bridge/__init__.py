import logging

from aiokafka import AIOKafkaConsumer
from websockets import ServerConnection, serve
import websockets


logger = logging.getLogger(__package__)


def create_kafka_consumer(kafka_address: str, kafka_topic_pattern: str) -> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(bootstrap_servers=kafka_address,
                                connections_max_idle_ms=None,
                                metadata_max_age_ms=1000)
    consumer.subscribe(pattern=kafka_topic_pattern)
    return consumer


async def start_kafka_websocket_bridge(handler, host: str, port: int) -> None:
    async with serve(handler, host, port) as server:
        logger.info("WebSocket server started!")
        await server.serve_forever()


async def kafka_websocket_handler(websocket: ServerConnection, consumer: AIOKafkaConsumer) -> None:
    websocket_remote_address = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    logger.info(f"WebSocket connection established from: {websocket_remote_address}")
    try:
        async for msg in consumer:
            await websocket.send(msg.value)
            logger.debug(f"Message sent to WebSocket client: {msg.value}")
    except websockets.exceptions.ConnectionClosedOK:
        logger.info("WebSocket client disconnected gracefully")
    except Exception as e:
        logger.error(f"Error in Kafka Websocket handler: {e}")
    finally:
        logger.info(f"WebSocket connection closed from: {websocket_remote_address}")
        await websocket.close()
