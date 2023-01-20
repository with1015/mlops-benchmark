#!/bin/bash

if [ $# -lt 2 ]; then
  echo "[USAGE] ./run_mlflow_benchmark.sh [Image] [Name]"
  exit 1
fi

bind_path=/home/mlops/mlops/mlflow
image=$1
name=$2

docker run -d -it --name $2 \
  --gpus "device=0" \
  --network=host \
  --mount type=bind,source=${bind_path},target=/workspace \
  $image
