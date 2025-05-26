from typing import Awaitable
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaConnectionError
from websockets import ServerConnection, serve


async def create_websocket_server(handler: Awaitable, host: str, port: int) -> None:
    async with serve(handler, host, port) as server:
        await server.serve_forever()


async def kafka_websocket_handler(websocket: ServerConnection, consumer: AIOKafkaConsumer) -> None:
    try:
        await consumer.start()
        async for msg in consumer:
            await websocket.send(msg.value)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()
        await websocket.close()
