#!/bin/bash

port=$1

curl -i \
  --header "Content-Type: image/jpeg" \
  --request POST \
  --data-binary @/home/mlops/mlops/flask/data/test_image.jpg \
  localhost:${port}/predict

echo ""
