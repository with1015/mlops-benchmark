#!/bin/bash

port=$1

curl -i \
  --header "Content-Type: Multipart/related" \
  --request POST \
  --data-binary @/home/mlops/mlops/flask/data/test_image.jpg \
  localhost:${port}/invocations

echo ""
