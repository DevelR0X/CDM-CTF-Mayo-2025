from Crypto.Util.number import GCD, bytes_to_long
from pwn import remote # pip install pwntools
import math

HOST = "0.0.0.0"
PORT = 1337

r = remote(HOST, PORT)

# Guardar firma en cache
r.sendlineafter(b"> ", b"1")
appointment = b"dcryp7;was_here;05-06-2025;18:00"
r.sendlineafter(b"> ", appointment)

# Limpiar cache
r.sendlineafter(b"> ", b"3")
r.sendlineafter(b"Ingrese su cita: ", appointment)
r.sendlineafter(b"Slot a limpiar: ", b"1") # da igual el que queramos limpiar

# Regenerar llaves para causar error en la firma de nuestro appointment inicial
r.sendlineafter(b"> ", b"4")
r.recvuntil(b"Llaves RSA regeneradas: ")
e, n = eval(r.recvline()[:-2].decode())

# Obtener firma con error (Fault)
r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"> ", appointment)
r.recvuntil(b"Firma digital: ")
s = eval(r.recvline()[:-1].decode())

# Recuperar p con el Fault Attack (GCD)
m = bytes_to_long(appointment)
p = GCD(pow(s, e, n) - m, n)
q = n // p

# Recuperar la llave privada
d = pow(e, -1, (p - 1) * (q - 1))

target_appointment = b"dcryp7;was_here;16-05-2025;08:00"
target_signature = pow(bytes_to_long(target_appointment), d, n) # Usar CRT o no, da lo mismo

r.sendlineafter(b"> ", b"2")
r.sendlineafter(b"Ingrese su cita: ", target_appointment)
r.sendlineafter(b"Ingrese la firma de su cita: ", str(target_signature).encode())

print(r.recv(1024))