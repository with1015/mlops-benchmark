#!/bin/bash

if [ $# -lt 2 ]; then
  echo 'USAGE: ./run_vision_server.sh [model] [mode]'
  exit 1
fi

model=$1
mode=$2

if [ $mode = "cpu" ]; then
  FLASK_DEBUG=1 python3 app_vision.py --model $model
else
  FLASK_DEBUG=1 python3 app_vision.py --model $model --gpu-mode
fi
