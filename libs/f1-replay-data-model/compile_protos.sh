#!/bin/bash

python_dir="./python/f1_replay_data_model_py"
typescript_dir="./typescript/src/lib"

protoc \
  --proto_path=./protos \
  --python_out="$python_dir" \
  --pyi_out="$python_dir" \
  --plugin=../../node_modules/ts-proto/protoc-gen-ts_proto \
  --ts_proto_opt=esModuleInterop=true \
  --ts_proto_out="$typescript_dir" \
  F1CarTelemetryReport.proto
