<?php
// Ruta de los archivos de almacenamiento
$votesFile = 'votes.txt';
$resultsFile = 'results.txt';

// Función para leer el archivo en un array
function readFileToArray($file) {
    if (!file_exists($file)) {
        return [];
    }
    return explode("\n", file_get_contents($file));
}

// Función para escribir un array en un archivo
function writeArrayToFile($file, $array) {
    file_put_contents($file, implode("\n", $array));
}

// Obtener datos del formulario
$email = $_POST["email"];
$team = $_POST["team"];

// Leer votos existentes
$votes = readFileToArray($votesFile);

// Verificar si el email ya ha votado
$emailAlreadyVoted = false;
foreach ($votes as $vote) {
    list($storedEmail, $storedTeam) = explode(':', $vote);
    if ($storedEmail == $email) {
        $emailAlreadyVoted = true;
        break;
    }
}

if ($emailAlreadyVoted) {
    echo "Usted ya ha respondido la encuesta.";
} else {
    // Añadir el email a la lista de votos
    $votes[] = "$email:$team";
    writeArrayToFile($votesFile, $votes);

    // Leer resultados actuales
    $results = readFileToArray($resultsFile);

    // Actualizar el conteo de votos
    $teamVotes = [];
    foreach ($results as $result) {
        list($teamName, $count) = explode(':', $result);
        $teamVotes[$teamName] = (int)$count;
    }

    if (!isset($teamVotes[$team])) {
        $teamVotes[$team] = 0;
    }
    $teamVotes[$team] += 1;

    // Guardar resultados actualizados
    $newResults = [];
    foreach ($teamVotes as $teamName => $count) {
        $newResults[] = "$teamName:$count";
    }
    writeArrayToFile($resultsFile, $newResults);

    // Mostrar resultados
    echo "<h2>Resultados de la encuesta:</h2>";
    echo "<table border='1'>";
    echo "<tr><th>Equipo</th><th>Votos</th></tr>";
    foreach ($teamVotes as $teamName => $count) {
        echo "<tr><td>" . htmlspecialchars($teamName) . "</td><td>" . htmlspecialchars($count) . "</td></tr>";
    }
    echo "</table>";
}
?>

