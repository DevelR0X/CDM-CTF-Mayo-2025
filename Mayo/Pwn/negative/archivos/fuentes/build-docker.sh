#!/bin/bash
NAME="negative"
docker build --tag=pwn_$NAME .
docker run -p 5152:1337 --rm --name=pwn_$NAME --detach --detach pwn_$NAME