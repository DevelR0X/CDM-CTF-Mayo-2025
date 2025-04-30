#!/bin/bash
NAME="shellcode2"
docker build --tag=pwn_$NAME .
docker run -p 5154:1337 --rm --name=pwn_$NAME --detach pwn_$NAME