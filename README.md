# Desafíos para el Campo de Marte CTF

#### Autores: 
* Daniel Espinoza (D-Cryp7), DevelR0X.

## Contenido

Cada desafío contiene las siguientes carpetas y archivos:
* `archivos`: Carpeta que contiene las siguientes subcarpetas:
    * `adjuntos`: Son los archivos que se deben adjuntar en la plataforma principal del CTF. Serán vistos por los participantes.
    * `fuentes`: Archivos necesarios para montar el docker de un reto online (interacción con servidor). Si el desafío es offline, se adjuntan los archivos que permiten replicar los archivos en la carpeta `adjuntos`. **El contenido de esta carpeta sólo debe ser visible para los revisores**.
    * `solucion`: Solución del desafío. **El contenido de esta carpeta sólo debe ser visible para los revisores**.
* `README.md`: Descripcion del reto, contexto y formato de la flag.
* `flag.txt`: Flag del desafio (**sólo visible para revisores**)

## Desafíos Mayo 2025

| Categoría | Nombre                           | Objetivo | Dificultad [⭐⭐⭐] |
| ---       | ---                              | ---      |   ---            |
| Crypto    | [Q-Locker](Mayo/Crypto/Q-Locker) | Explotar un _Known Plaintext Attack_ en la operacion XOR, que es equivalente a la compuerta cuantica CNOT, para desencriptar archivos.       | ⭐⭐ |
| Crypto    | [LJWT](Mayo/Crypto/LJWT)         | Recuperar la llave privada con la que se contruyen LJWTs para ingresar al sistema como administrador. Un _Linear_ JSON Web Token (JWT) es un algoritmo personalizado que utiliza un esquema afin para computar cada firma digital. Asi pues, dos cuentas registradas son suficientes para recuperar la llave privada del servidor. | ⭐⭐ |
| Crypto    | [Waiting List I](Mayo/Crypto/Waiting%20List%20I) | Explotar el _Fermat Factorization Attack_ en RSA para firmar una cita antes que el resto de pacientes y ser atendido inmediatamente. | ⭐⭐ |
| Crypto    | [Waiting List II](Mayo/Crypto/Waiting%20List%20II) | Explotar el _Fault Attack_ en RSA para firmar una cita antes que el resto de pacientes y ser atendido inmediatamente. | ⭐⭐⭐ |