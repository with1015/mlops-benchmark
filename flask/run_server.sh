#!/bin/bash

if [ $# -lt 1 ]; then
  echo 'USAGE: ./run_server.sh [model]'
  exit 1
fi

model=$1

FLASK_ENV=development python3 app.py --model $model --gpu-mode
