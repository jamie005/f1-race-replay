import asyncio
from aiokafka import AIOKafkaConsumer
from websockets.asyncio.server import serve



async def echo(websocket):
    consumer = AIOKafkaConsumer(
        'f1-race-replay.telemetry.ver',
        bootstrap_servers='localhost:9094')
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            await websocket.send(msg.value)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()
        

async def main():
    async with serve(echo, "localhost", 8765) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
