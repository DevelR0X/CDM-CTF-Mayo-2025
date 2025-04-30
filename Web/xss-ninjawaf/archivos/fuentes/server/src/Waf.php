<?php
/**
 * name....: Challenge XSS WAF Bypass 
 * author..: Esteban XFCE - Develrox
 * date....: 04-2025
 * 
 **/

class Waf
{
    public static function sanitize_invisible_chars($raw_string)
    {
        // Lista de caracteres invisibles comunes
        $invisibles = [
            "\n", // Salto de línea
            "\r", // Retorno de carro
            "\t", // Tabulador
            "\0", // Null byte
            "\x0B", // Vertical tab
            "\x0C", // Form feed
            "\xA0", // Espacio no separable (NBSP)
            "\x{200B}", // Zero width space
            "\x{200C}", // Zero width non-joiner
            "\x{200D}", // Zero width joiner
            "\x{FEFF}", // Byte Order Mark (BOM)
        ];

        $raw_string = str_replace($invisibles, " ", $raw_string);

        // Eliminamos cualquier carácter de control adicional (ASCII 0-31 excepto 9)
        $raw_string = preg_replace(
            '/[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]/u',
            " ",
            $raw_string
        );

        return trim($raw_string);
    }

    public static function validate_chars($raw_string)
    {

        // Blacklist documentada y agrupada por categoría
        $blacklist = [

            // Funciones emergentes y ejecución directa
            'alert', 'prompt', 'confirm', 'eval', 'print', 'return', 
            'Function.bind', 'setTimeout', 'setInterval', 'queueMicrotask', 'requestAnimationFrame',

            // Manipulación de navegación
            'open', 'close', 'blur', 'focus', 'moveTo', 'moveBy', 'resizeTo', 'resizeBy',
            'scrollTo', 'scrollBy', 'location.assign', 'location.replace', 'location.reload',

            // APIs con salida visual o auditiva
            'Audio', 'SpeechSynthesisUtterance', 'speechSynthesis',

            // Objetos globales
            'document', 'window', 'navigator', 'location',
            'parent', 'top', 'frames', 'opener', 'self',

            // Propiedades sensibles del DOM
            'innerHTML', 'outerHTML', 'textContent', 'value', 'cookie',

            // Eventos HTML comunes
            'onerror', 'onload', 'onclick', 'onmouseover', 'onfocus', 'onblur', 'onsubmit',

            // Elementos HTML que permiten inyección
            'iframe', 'img', 'script', 'svg', 'math', 'body', 'head', 'meta', 'style', 'link', 'base',

            // Evasión a través de prototipos
            'constructor', '__proto__', 'prototype', 'bind', 'call', 'apply', 'name',

            // Funciones de escape y codificación
            'escape', 'unescape', 'encode', 'decode', 'btoa', 'atob',

            // Funciones avanzadas del lenguaje
            'import', 'new', 'class', 'Reflect', 'Proxy', 'Object', 'Array', 'Map', 'WeakMap', 'RegExp',
            'assign', 'defineProperty', 'defineProperties', 'hasOwnProperty',

            // Métodos de strings
            'split', /*'slice', */ 'match', /*'replace', */ 'search', 'indexOf', 'includes', 'substring', 'substr',

            // Construcción dinámica con códigos de caracteres
            /*'fromCharCode', 'fromCodePoint', 'charCodeAt', 'codePointAt', 'charAt',*/

            // Funciones para llamadas HTTP
            'XMLHttpRequest', 'fetch', 'axios', 'got', 'ajax', 'navigator', 'request', 

            // Caracteres especiales y comúnmente usados en evasión
            '<', '>', '`', "'", '+', '[', ']', '{', '}', '%', '\\', '/', '#', '@', '&', '^', '|', '~', ':', '?', '!', /*',',*/ '*', '$', '='
        ];

        foreach ($blacklist as $bad)
        {
            if (preg_match('/' . preg_quote($bad, '/') . '/i', $raw_string))
            {
                //die("Bloqueado por uso de patrón prohibido: <code>" . htmlspecialchars($bad) . "</code>");
                die("<code>WAF-tronic 4000 -> Payload stoped.</code>");
            }
        }
    }
}
