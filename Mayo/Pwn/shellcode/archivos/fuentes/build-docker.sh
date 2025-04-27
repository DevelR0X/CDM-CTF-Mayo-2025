#!/bin/bash
NAME="shellcode"
docker build --tag=pwn_$NAME .
docker run -p 5153:1337 --rm --name=pwn_$NAME --detach pwn_$NAME