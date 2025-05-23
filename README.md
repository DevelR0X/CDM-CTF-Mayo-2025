<p align = 'center'>
  <img src = 'assets/logo.svg' alt = "DevelR0X">
</p>

## Autores:

* Daniel Espinoza (D-Cryp7), _DevelR0X_.
* Borja Gomez (kub0x), _DevelR0X_.
* Esteban Vaquero (Esteban XFCE), _DevelR0X_.

## Contenido

Cada desafío contiene las siguientes carpetas y archivos:
* `archivos`: Carpeta que contiene las siguientes subcarpetas:
    * `adjuntos`: Son los archivos que se deben adjuntar en la plataforma principal del CTF. Serán vistos por los participantes.
    * `fuentes`: Archivos necesarios para montar el docker de un reto online (interacción con servidor). Si el desafío es offline, se adjuntan los archivos que permiten replicar los archivos en la carpeta `adjuntos`. **El contenido de esta carpeta sólo debe ser visible para los revisores**.
    * `solucion`: Solución del desafío. **El contenido de esta carpeta sólo debe ser visible para los revisores**.
* `README.md`: Descripcion del reto, contexto y formato de la flag.
* `flag.txt`: Flag del desafio (**sólo visible para revisores**)

## Desafíos

| Categoría | Nombre                           | Objetivo | Dificultad [⭐⭐⭐] |
| ---       | ---                              | ---      |   ---            |
| Misc    | [Command](Misc/command) | Llamada a system() bajo ls "input". El atacante ha de introducir un _command injection_ típico.      | ⭐ |
| Misc    | [Q-Locker](Misc/Q-Locker) | Explotar un _Known Plaintext Attack_ en la operación XOR, que es equivalente a la compuerta cuántica CNOT, para desencriptar archivos.       | ⭐⭐ |
| Crypto    | [Waiting List I](Crypto/Waiting%20List%20I) | Explotar el _Fermat Factorization Attack_ en RSA para firmar una cita antes que el resto de pacientes y ser atendido inmediatamente. | ⭐⭐ |
| Crypto    | [Waiting List II](Crypto/Waiting%20List%20II) | Explotar el _Fault Attack_ en RSA para firmar una cita antes que el resto de pacientes y ser atendido inmediatamente. | ⭐⭐⭐ |
| Web    | [CTTP](Web/cttp)         | WebServer en C parseando \r\n (CRLF). Configurado sólo para un endpoint que es vulnerable a path traversal. | ⭐ |
| Web    | [LJWT](Web/LJWT)         | Recuperar la llave privada con la que se contruyen LJWTs para ingresar al sistema como administrador. Un _Linear_ JSON Web Token (JWT) es un algoritmo personalizado que utiliza un esquema afín para computar cada firma digital. Así pues, dos cuentas registradas son suficientes para recuperar la llave privada del servidor. | ⭐⭐⭐ |
| Web    | [XSS-NinjaWAF](Web/xss-ninjawaf) | Explotar un XSS para el robo de cookies de sesión aplicando técnicas de evasión de WAF.  | ⭐⭐ |
| Pwn    | [Shellcode](Pwn/shellcode)   | El programa ejecuta directamente el input por lo que se debe introducir una shellcode.  | ⭐ |
| Pwn    | [LeakMe](Pwn/LeakMe) | Un leak típico. Dos cadenas declaradas en el stack. Se debe hacer overlapping para imprimir el contenido de ambas.  | ⭐ |
| Pwn    | [Negative](Pwn/negative) | Se declara un buffer y un byte 'admin' en 0x0. Si éste se pone en 0x1 nos entrega la flag. El programa acepta una posición donde escribiremos dentro del buffer. Si la posición se desborda podemos escribir arriba del buffer (posición negativa) y sobreescribir el byte 'admin' a 0x1.  | ⭐⭐ |
| Pwn    | [Shellcode2](Pwn/shellcode2) | El programa ejecuta directamente el input por lo que se debe introducir una shellcode que evada el filtro definido deltro del código fuente.  | ⭐⭐ |
| Pwn    | [Citas](Pwn/citas) | Sistema de Citas en C. Se dan de alta usuarios por nombre y apellido, guardando sus datos en una linked-list. Existe el parámetro admin en cada usuario que está por defecto en 0. La idea es ver como lekear y sobreescribirlo a 1.  | ⭐⭐⭐ |
