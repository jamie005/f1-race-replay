FROM python:3.11.12-alpine3.21

COPY ./apps/f1-car-data-stub/dist/f1_car_data_stub-1.0.0-py3-none-any.whl /app/f1_car_data_stub-0.1.0-py3-none-any.whl

WORKDIR /app

RUN pip install --no-cache-dir f1_car_data_stub-0.1.0-py3-none-any.whl

CMD ["python", "-m", "f1_car_data_stub"]
