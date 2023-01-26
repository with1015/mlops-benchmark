#!/bin/bash

# Setting service for deployments
kubectl apply -f set_canary_svc.yaml
kubectl apply -f canary-rule.yaml
kubectl apply -f set_virtual_service.yaml

# Deploy models
kubectl apply -f kserve_v1.yaml
kubectl apply -f kserve_v2.yaml

# Deploy request pod
kubectl apply -f send-request.yaml

kubectl exec -it http-send -- bash
