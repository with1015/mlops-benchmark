# Serving framework benchmark for MLOps

## Requirements
1. Docker >= 20.10.22
2. Kubernetes == 1.21 (recommend for Canary test)

## How to run
1. Build docker image in framework directory
2. Run benchmark script file.
3. Send inference request to server.

#### Example for ResNet-18 with Flask
```
cd ~/mlops-benchamrk/flask
docker build -f Docker.vision --tag with1015/flask-resnet18-gpu .
cd ~/mlops-benchamrk
./run_flask_benchmark.sh with1015/flask-resnet18-gpu flask-test
```
