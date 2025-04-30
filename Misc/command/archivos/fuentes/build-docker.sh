#!/bin/bash
NAME="command"
docker build --tag=misc_$NAME .
docker run -p 5150:1337 --rm --name=misc_$NAME --detach misc_$NAME