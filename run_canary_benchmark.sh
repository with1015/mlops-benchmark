#!/bin/bash

docker build -f ./flask/Dockerfile.resnet18 --tag with1015/flask-resnet18 .
docker build -f ./kserve/Dockerfile.vision --tag with1015/kserve-resent18 .

kubectl apply -f ./flask/flask_v1.yaml
kubectl apply -f ./kserve/kserve_v2.yaml
kubectl apply -f ./set_canary.yaml
