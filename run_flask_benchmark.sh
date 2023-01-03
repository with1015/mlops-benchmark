#!/bin/bash

bind_path=/home/mlops/mlops/flask
image=pytorch/pytorch:1.8.1-cuda11.1-cudnn8-devel

docker run -d -it --name $1 \
  --gpus "device=0" \
  -p 5000:5000 \
  --mount type=bind,source=${bind_path},target=/root \
  $image
