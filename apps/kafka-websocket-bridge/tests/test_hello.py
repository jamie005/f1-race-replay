"""Hello unit test module."""

from kafka_websocket_bridge.hello import hello


def test_hello():
    """Test the hello function."""
    assert hello() == "Hello kafka-websocket-bridge"
