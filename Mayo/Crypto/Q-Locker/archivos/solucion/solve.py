from itertools import cycle

FILES = [
    "objetivos.md",
    "etica.md",
    "incidentes.md"
]

# Podemos usar nuestro propio XOR u otro que queramos, lo importante es hacer XOR a nivel de bytes
# ademas de que se reutilice a o b
# el XOR de pwntools esta bien tambien
def xor(a, b):
    return bytes([ x ^ y for x, y in zip(a, cycle(b)) ])

def decrypt_files(files):
    # Lo importante aqui es saber que un CNOT es un XOR
    # Ademas, todos los mensajes parten con "Q-LOCKER v1.0 (2025)", por lo que podemos derivar la llave:
    # llave = documento_encriptado XOR "Q-LOCKER v1.0 (2025)"
    # Lo que se conoce como Known Plaintext Attack.

    known = b"Q-LOCKER v1.0 (2025)"
    encrypted_file = open(f"ENCRYPTED_{files[0].split('.')[0]}", "rb").read()
    key = xor(known[:16], encrypted_file[:16])

    # Ahora desencriptamos todos los archivos
    for file in files:
        encrypted_file = open(f"ENCRYPTED_{file.split('.')[0]}", "rb").read()
        decrypted_file = xor(encrypted_file, key)

        recovered_file = open(file, "wb")
        recovered_file.write(decrypted_file[20:])
        recovered_file.close()

decrypt_files(FILES)