#!/bin/bash
NAME="leakme"
docker build --tag=pwn_$NAME .
docker run -it -p 5151:1337 --rm --name=pwn_$NAME --detach pwn_$NAME