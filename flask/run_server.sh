#!/bin/bash

if [ $# -lt 2 ]; then
  echo 'USAGE: ./run_server.sh [model] [mode]'
  exit 1
fi

model=$1
mode=$2

if [ $mode = "cpu" ]; then
  FLASK_DEBUG=development python3 app.py --model $model
else
  FLASK_DEBUG=development python3 app.py --model $model --gpu
fi
