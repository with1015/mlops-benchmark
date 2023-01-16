#!/bin/bash

if [ $# -lt 2 ]; then
  echo "[USAGE] ./run_kserve_benchmark.sh [Image] [Name]"
  exit 1
fi

bind_path=/home/mlops/mlops/kserve
image=$1
name=$2

docker run -d -it --name $name \
  -ePORT=8080 -p8080:8080 \
  --gpus "device=0" \
  --mount type=bind,source=${bind_path},target=/workspace \
  $image
