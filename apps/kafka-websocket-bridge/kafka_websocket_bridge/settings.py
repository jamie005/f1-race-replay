from f1_replay_py_helpers.settings import BaseKafkaServiceSettings


class KafkaWebsocketBridgeSettings(BaseKafkaServiceSettings):
    websocket_host: str = "localhost"
    websocket_port: int = 8765
    kafka_topic_pattern: str = "f1-race-replay.telemetry.*"
