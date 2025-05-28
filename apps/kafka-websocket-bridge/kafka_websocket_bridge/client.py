import asyncio
import logging
from websockets.asyncio.client import connect

from f1_replay_py_helpers.logging import color_log_handler


async def main():
        # Default WARNING level logger setup
    logger = logging.getLogger(__package__)
    logger.addHandler(color_log_handler)
    logger.setLevel(logging.INFO)  # Set to INFO for more detailed output

    async with connect("ws://localhost:8765") as websocket:
        async for message in websocket:
            logger.info("Received a message!")

if __name__ == "__main__":
    asyncio.run(main())
