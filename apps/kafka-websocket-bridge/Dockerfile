FROM python:3.11.12-slim-bullseye

WORKDIR /app

COPY ./apps/kafka-websocket-bridge/dist/kafka_websocket_bridge-1.0.0-py3-none-any.whl  . 

RUN pip install --no-cache-dir kafka_websocket_bridge-1.0.0-py3-none-any.whl

CMD ["python", "-m", "kafka_websocket_bridge"]
