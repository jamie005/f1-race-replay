import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from kafka_websocket_bridge import create_kafka_websocket_bridge, kafka_websocket_handler


@pytest.mark.asyncio
async def test_kafka_websocket_handler_sends_messages():
    # Mock websocket and consumer
    websocket = AsyncMock()
    consumer = AsyncMock()
    consumer.__aiter__.return_value = [MagicMock(value=b"msg1"), MagicMock(value=b"msg2")]

    await kafka_websocket_handler(websocket, consumer)

    websocket.send.assert_any_await(b"msg1")
    websocket.send.assert_any_await(b"msg2")
    websocket.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_kafka_websocket_handler_handles_exception():
    websocket = AsyncMock()
    consumer = AsyncMock()
    consumer.__aiter__.side_effect = Exception("fail")

    with pytest.raises(Exception):
        await kafka_websocket_handler(websocket, consumer)

    websocket.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_kafka_websocket_bridge_calls_serve_forever():
    handler = AsyncMock()
    with patch("kafka_websocket_bridge.serve") as mock_serve:
        mock_server = AsyncMock()
        mock_serve.return_value.__aenter__.return_value = mock_server

        # Run only a short time to avoid infinite loop
        async def fake_serve_forever():
            await asyncio.sleep(0.01)
        mock_server.serve_forever.side_effect = fake_serve_forever

        await create_kafka_websocket_bridge(handler, "localhost", 1234)
        mock_serve.assert_called_with(handler, "localhost", 1234)
        mock_server.serve_forever.assert_awaited_once()
