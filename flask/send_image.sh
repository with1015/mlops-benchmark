#!/bin/bash

url=127.0.0.1
port=50000

python3 request_test.py \
  --url $url \
  --port $port \
  --image './data/test_image.jpg'
