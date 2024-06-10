<?php
  // Ruta de los archivos de almacenamiento
  $votesFile = './encuesta/votes.txt';
  $resultsFile = './encuesta/results.txt';
  $votesFile = '/home/william/Documentos/Encuesta/votes.txt';
  $resultsFile = '/home/william/Documentos/Encuesta/results.txt';

  // Función para leer el archivo en un array
  function readFileToArray($file) {
    if (!file_exists($file)) {
      // Crear archivo si no existe
      file_put_contents($file, '');
      return [];
    }
    return explode("\n", trim(file_get_contents($file)));
  }

  // Función para escribir un array en un archivo
  function writeArrayToFile($file, $array) {
    file_put_contents($file, implode("\n", $array));
  }

  // Obtener datos del formulario
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST["email"];
    $team = $_POST["team"];

    // Leer votos existentes
    $votes = readFileToArray($votesFile);

    // Verificar si el email ya ha votado
    if (in_array($email, $votes)) {
      echo "Usted ya ha respondido la encuesta.";
    } else {
      // Añadir el email a la lista de votos
      $votes[] = $email;
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
        echo "<tr><td>$teamName</td><td>$count</td></tr>";
      }
      echo "</table>";
    }
  } else {
    echo "Método de solicitud no válido.";
  }
?>