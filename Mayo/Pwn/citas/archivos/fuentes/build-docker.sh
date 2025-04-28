#!/bin/bash
NAME="hidden"
docker build --tag=pwn_$NAME .
docker run -p 5156:1337 --rm --name=pwn_$NAME --detach --detach pwn_$NAME