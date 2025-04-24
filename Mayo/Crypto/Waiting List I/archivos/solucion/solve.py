from Crypto.Util.number import bytes_to_long
from pwn import remote # pip install pwntools
import math

def is_perfect_square(n):
    root = int(math.isqrt(n))
    return root * root == n

def fermat_factor(N, max_iter = 1000000):
    a = math.isqrt(N)
    if a * a < N:
        a += 1
    for _ in range(max_iter):
        b2 = a * a - N
        if is_perfect_square(b2):
            b = math.isqrt(b2)
            p = a - b
            q = a + b
            if p * q == N:
                return p, q
        a += 1
    return None, None

HOST = "0.0.0.0"
PORT = 1337

r = remote(HOST, PORT)

init = "Llave pública: "
r.recvuntil(init.encode())

e, n = eval(r.recvline()[:-1].decode())

p, q = fermat_factor(n)

d = pow(e, -1, (p - 1) * (q - 1))

appointment = b"dcryp7;was_here;16-05-2025;08:00"
m = bytes_to_long(appointment)
signature = pow(m, d, n)

r.sendlineafter(b"> ", b"2")
r.sendlineafter(b"Ingrese su cita: ", appointment)
r.sendlineafter(b"Ingrese la firma de su cita: ", str(signature).encode())

print(r.recv(1024))