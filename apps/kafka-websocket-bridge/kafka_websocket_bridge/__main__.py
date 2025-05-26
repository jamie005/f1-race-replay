import asyncio
import functools
from aiokafka import AIOKafkaConsumer

from kafka_websocket_bridge import create_websocket_server, kafka_websocket_handler
from kafka_websocket_bridge.settings import KafkaWebsocketBridgeSettings


async def main():
    settings = KafkaWebsocketBridgeSettings()

    consumer = AIOKafkaConsumer(bootstrap_servers=settings.kafka_address,)
    consumer.subscribe(pattern=settings.kafka_topic_pattern)

    handler = functools.partial(kafka_websocket_handler, consumer=consumer)
    
    await create_websocket_server(handler, host=settings.websocket_host, port=settings.websocket_port)


if __name__ == "__main__":
    asyncio.run(main())
