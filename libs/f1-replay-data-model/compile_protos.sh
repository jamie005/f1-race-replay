#!/bin/bash

protos_dir="./protos"
python_dir="./python/f1_replay_data_model_py"
typescript_dir="./typescript/src"

# Array of proto file names defined
readarray -t proto_files < <(find ${protos_dir} -type f -name "*.proto")

# Protos compiled for both 
protoc \
  --proto_path="$protos_dir" \
  --python_out="$python_dir" \
  --pyi_out="$python_dir" \
  --plugin=../../node_modules/ts-proto/protoc-gen-ts_proto \
  --ts_proto_opt=esModuleInterop=true,outputIndex=true \
  --ts_proto_out="$typescript_dir" \
  "${proto_files[@]}"
