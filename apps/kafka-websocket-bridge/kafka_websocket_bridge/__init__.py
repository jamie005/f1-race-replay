from aiokafka import AIOKafkaConsumer
from websockets import ServerConnection, serve


def create_kafka_consumer(kafka_address: str, kafka_topic_pattern: str) -> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(bootstrap_servers=kafka_address,
                                connections_max_idle_ms=None,
                                metadata_max_age_ms=1000)
    consumer.subscribe(pattern=kafka_topic_pattern)
    return consumer


async def create_kafka_websocket_bridge(handler, host: str, port: int) -> None:
    async with serve(handler, host, port) as server:
        await server.serve_forever()


async def kafka_websocket_handler(websocket: ServerConnection, consumer: AIOKafkaConsumer) -> None:
    try:
        async for msg in consumer:
            await websocket.send(msg.value)
    finally:
        await websocket.close()
