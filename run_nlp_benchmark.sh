#!/bin/bash

bind_path=/home/mlops/mlops/gpt-test
image=nlp:latest

docker run -d -it --name $1 \
  --gpus "device=0" \
  --network=host \
  --mount type=bind,source=${bind_path},target=/workspace \
  $image
