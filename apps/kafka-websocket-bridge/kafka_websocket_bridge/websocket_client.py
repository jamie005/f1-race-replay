import asyncio
import logging
from websockets.asyncio.client import connect

from f1_replay_data_model_py.F1CarTelemetryReport_pb2 import F1CarTelemetryReport
from f1_replay_py_helpers.logging import color_log_handler


async def main():
    logger = logging.getLogger(__package__)
    logger.addHandler(color_log_handler)
    logger.setLevel(logging.INFO)

    async with connect("ws://localhost:8765") as websocket:
        async for message in websocket:
            logger.info(f"Received a message:\n{F1CarTelemetryReport.FromString(message)}")


if __name__ == "__main__":
    asyncio.run(main())
