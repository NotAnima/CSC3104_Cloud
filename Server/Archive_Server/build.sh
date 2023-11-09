#!/bin/bash
docker build -t dereknan/cloud-server-arm64:latest -f Dockerfile.arm64 .
docker push dereknan/cloud-server-arm64:latest 
