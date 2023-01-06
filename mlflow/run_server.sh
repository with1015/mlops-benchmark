#!/bin/bash

model_path=$1

if [ $# -lt 1 ]; then
  echo "USAGE: ./run_server.sh [model path]"
  exit 1
fi

mlflow models serve -m ${model_path}_pretrained --env-manager=local 
