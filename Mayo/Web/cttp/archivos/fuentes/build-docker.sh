#!/bin/bash
NAME="ctpp"
docker build --tag=web_$NAME .
docker run -p 5155:1337 --rm --name=web_$NAME --detach web_$NAME