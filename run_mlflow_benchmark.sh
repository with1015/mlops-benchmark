#!/bin/bash

bind_path=/home/mlops/mlops/mlflow
image=$1

if [ $# -lt 2 ]; then
  echo "[USAGE] ./run_mlflow_benchmark.sh [Image] [Name]"
  exit 1
fi

docker run -d -it --name $2 \
  --gpus "device=0" \
  --network=host \
  --mount type=bind,source=${bind_path},target=/workspace \
  $image
