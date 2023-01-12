#!/bin/bash

if [ $# -lt 2 ]; then
  echo 'USAGE: ./run_gpt_server.sh [model] [mode]'
  exit 1
fi

model=$1
mode=$2

if [ $mode = "cpu" ]; then
  FLASK_DEBUG=development python3 app_gpt.py --model $model
else
  FLASK_DEBUG=development python3 app_gpt.py --model $model --gpu-mode
fi
