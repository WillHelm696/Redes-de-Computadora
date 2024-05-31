<?php
  // Database connection (replace with your actual credentials)
  $servername = "localhost";
  $username = "your_username";
  $password = "your_password";
  $dbname = "your_database";

  $conn = new mysqli($servername, $username, $password, $dbname);

  // Check connection
  if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
  }

  // Get form data
  $email = $_POST["email"];
  $team = $_POST["team"];

  // Check if email already exists in the database
  $sql = "SELECT * FROM votes WHERE email = '$email'";
  $result = $conn->query($sql);

  if ($result->num_rows > 0) {
    echo "Usted ya ha respondido la encuesta.";
  } else {
    // Insert vote into the database
    $sql = "INSERT INTO votes (email, team) VALUES ('$email', '$team')";
    if ($conn->query($sql) === TRUE) {
      // Update team vote count
      $sql = "UPDATE teams SET votes = votes + 1 WHERE name = '$team'";
      $conn->query($sql);

      // Fetch vote results
      $sql = "SELECT * FROM teams";
      $result = $conn->query($sql);

      // Display results
      echo "<h2>Resultados de la encuesta:</h2>";
      echo "<table border='1'>";
      echo "<tr><th>Equipo</th><th>Votos</th></tr>";
      while($row = $result->fetch_assoc()) {
        echo "<tr><td>" . $row["name"] . "</td><td>" . $row["votes"] . "</td></tr>";
      }
      echo "</table>";
    } else {
      echo "Error: " . $sql . "<br>" . $conn->error;
    }
  }

  $conn->close();
?>