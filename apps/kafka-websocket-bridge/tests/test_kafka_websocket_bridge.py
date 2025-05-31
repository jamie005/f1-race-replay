import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import ConsumerStoppedError
from websockets import ServerConnection

from kafka_websocket_bridge import start_kafka_websocket_bridge, kafka_websocket_handler


@pytest.fixture
def mock_kafka_consumer() -> AIOKafkaConsumer:
    return AsyncMock()


@pytest.fixture
def mock_websocket() -> ServerConnection:
    return AsyncMock()


@pytest.mark.asyncio
async def test_kafka_websocket_handler_sends_messages(mock_kafka_consumer, mock_websocket):
    mock_kafka_consumer.__aiter__.return_value = [MagicMock(value=b"msg1"), MagicMock(value=b"msg2")]

    await kafka_websocket_handler(mock_websocket, mock_kafka_consumer)

    mock_websocket.send.assert_any_await(b"msg1")
    mock_websocket.send.assert_any_await(b"msg2")
    mock_websocket.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_kafka_websocket_handler_handles_exception(mock_kafka_consumer, mock_websocket, caplog):
    mock_kafka_consumer.__aiter__.side_effect = ConsumerStoppedError()

    with caplog.at_level("ERROR"):
        await kafka_websocket_handler(mock_websocket, mock_kafka_consumer)

    mock_websocket.close.assert_awaited_once()
    assert any("Error in Kafka Websocket handler" in record.message for record in caplog.records)


@pytest.mark.asyncio
async def test_start_kafka_websocket_bridge_calls_serve_forever():
    mock_server = AsyncMock()
    handler = AsyncMock()

    async def fake_serve_forever():
        await asyncio.sleep(0.01)
    with patch("kafka_websocket_bridge.serve") as mock_serve:
        mock_serve.return_value.__aenter__.return_value = mock_server
        mock_server.serve_forever.side_effect = fake_serve_forever

        await start_kafka_websocket_bridge(handler, "localhost", 1234)

        mock_serve.assert_called_with(handler, "localhost", 1234)
        mock_server.serve_forever.assert_awaited_once()
