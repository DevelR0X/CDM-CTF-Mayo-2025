<?php
/**
 * name....: Challenge XSS WAF Bypass 
 * author..: Esteban XFCE - Develrox
 * date....: 04-2025
 * 
 **/

error_reporting(0);
ini_set('display_errors', '0');

require_once __DIR__ . "/PCRDatabase.php";
require_once __DIR__ . "/Waf.php";

$flag   = getenv("FLAG_CONTENT") ?? "";
$dbname = getenv("DB_NAME") ?? "";

if (empty($flag)) {
    die("FATAL ERROR: FLAG NOT SET");
}

if (empty($dbname)) {
    die("FATAL ERROR: DB NOT SET");
}

$db  = new PCRDatabase($dbname);
$waf = new Waf();

if (isset($_GET["__b"])) {
    if ($_GET["__b"] == "3b93148f-1f52-4467-a6b0-e525fb6a9afe") {
        setcookie("session", $flag);
    }
} else {
    setcookie("session", "VISITOR");
}

// Procesar formulario si se envió
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $fecha = date("d-m-Y H:i:s");
    $folio = $_POST["folio"] ?? "";
    $resultado = $_POST["resultado"] ?? "";

    if ($fecha && $folio && $resultado) {
        // Recorte a longitudes máximas
        $folio = substr($folio, 0, 6);
        $resultado = substr($resultado, 0, 180);

        $folio = sprintf("PCR-%d-%d", $folio, time());
        $folio = $waf::sanitize_invisible_chars($folio);
        $resultado = $waf::sanitize_invisible_chars($resultado);
        $waf::validate_chars($resultado);

        $db->insertTest($fecha, $folio, $resultado);
        header("Location: " . $_SERVER["PHP_SELF"]);
        exit();
    }
}

// Configuración de paginación
$page = isset($_GET["page"]) ? max(1, (int) $_GET["page"]) : 1;
$pageSize = 5; // Cantidad de resultados por página
$tests = $db->getTests($page, $pageSize);
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Resultados PCR</title>
    <style>
        body {
          background-color: #c0c0c0;
          font-family: "Segoe UI", Tahoma, Geneva, sans-serif;
          color: #000;
          margin: 20px;
        }

        h1,
        h2 {
          background-color: #000080;
          color: white;
          padding: 6px;
          font-size: 18px;
          border: 2px outset #fff;
          width: fit-content;
        }

        form,
        table {
          background-color: #f0f0f0;
          padding: 10px;
          border: 2px ridge #ccc;
          margin-bottom: 20px;
          width: fit-content;
        }

        input[type="text"],
        input[type="date"],
        textarea {
          background-color: white;
          border: 2px inset #aaa;
          padding: 2px 4px;
          font-family: monospace;
          font-size: 14px;
        }

        button {
          background-color: #e0e0e0;
          border: 2px outset #fff;
          font-weight: bold;
          padding: 4px 10px;
          font-family: sans-serif;
          cursor: pointer;
        }

        button:hover {
          background-color: #dcdcdc;
        }

        table {
          border-collapse: collapse;
          font-size: 14px;
        }

        table th,
        table td {
          border: 1px solid #888;
          padding: 6px 10px;
          text-align: left;
          background-color: #fff;
        }

        a {
          color: blue;
          text-decoration: none;
          font-weight: bold;
        }

        a:hover {
          text-decoration: underline;
        }

        hr {
          border: none;
          height: 2px;
          background: #888;
          margin: 20px 0;
        }
    </style>
</head>
<body>

<h1>Agregar nueva prueba PCR</h1>
<form method="post" action="">
    <label>Folio:
        <input type="text" name="folio" required>
    </label><br><br>

    <label>Resultado:
        <textarea name="resultado" rows="4" cols="40" required></textarea>
    </label><br><br>

    <button type="submit">Guardar</button>
</form>

<hr>

<h2>Listado de pruebas</h2>

<table border="1" cellpadding="5" cellspacing="0">
    <thead>
        <tr>
            <th>Fecha</th>
            <th>Folio</th>
            <th>Resultado</th>
        </tr>
    </thead>
    <tbody>
    <?php if (count($tests) > 0): ?>
        <?php foreach ($tests as $test): ?>
            <tr>
                <td><?php echo htmlspecialchars($test['fecha']); ?></td>
                <td><?php echo htmlspecialchars($test['folio']); ?></td>
                <td><?php echo nl2br(htmlspecialchars($test['resultado']));?></td>
            </tr>
        <?php endforeach; ?>
    <?php else: ?>
        <tr><td colspan="3">No hay resultados.</td></tr>
    <?php endif; ?>
    </tbody>
</table>

<h2>Últimas pruebas positivas</h2>

<table border="1" cellpadding="5" cellspacing="0" id="last-positive">
    <thead>
        <tr>
            <th>Folio</th>
        </tr>
    </thead>
    <tbody>
    </tbody>
</table>

<br>

<div>
    <?php if ($page > 1): ?>
        <a href="?page=<?php echo $page - 1; ?>">← Anterior</a>
    <?php endif; ?>

    <strong> Página <?php echo $page; ?> </strong>

    <?php if (count($tests) === $pageSize): ?>
        <a href="?page=<?php echo $page + 1; ?>">Siguiente →</a>
    <?php endif; ?>
</div>


<script>
    let positiveResults = [];
    <?php if (count($tests) > 0) {
        foreach ($tests as $id => $test) {
            if (preg_match("/positivo/i", $test["resultado"])) {
                echo sprintf(
                    'let result_%d_folio = "%s"; ',
                    $id,
                    $test["folio"]
                );
                echo sprintf(
                    "let result_%d_resultado = \"%s\";\n",
                    $id,
                    $test["resultado"]
                );
                echo sprintf(
                    "positiveResults.push({\"resultado\":result_%d_resultado, \"folio\": result_%d_folio});\n",
                    $id, $id
                );
            }
        }
    } ?>

    let tbody = document.querySelector("#last-positive tbody");

    positiveResults.forEach(item => {
        let tr = document.createElement("tr");
        let td = document.createElement("td");
        td.textContent = item.folio;
        tr.appendChild(td);
        tbody.appendChild(tr);
    });
</script>
</body>
</html>