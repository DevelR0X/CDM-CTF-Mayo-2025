#!/bin/bash
NAME="ljwt"
docker rm -f crypto_$NAME
docker build --tag=crypto_$NAME . && \
docker run -p 5000:5000 --rm --name=crypto_$NAME --detach crypto_$NAME