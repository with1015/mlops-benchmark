#!/bin/bash

bind_path=/home/mlops/mlops/flask
image=flask-benchmark

docker run -d -it --name $1 \
  --gpus "device=0" \
  --network=host \
  --mount type=bind,source=${bind_path},target=/workspace \
  $image
