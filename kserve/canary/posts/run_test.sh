#!/bin/bash

if [ $# -lt 1 ]; then
  echo "[USAGE] ./run_test.sh [# of requests (int)]"
  exit 1
fi

max_iter=$1

for i in $(seq ${max_iter});
do
  python3 send-request.py
done
