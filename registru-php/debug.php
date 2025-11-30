<?php
// Debug script - arata toate erorile
error_reporting(E_ALL);
ini_set('display_errors', 1);

echo "<h1>DEBUG TEST</h1>";
echo "<p>PHP Version: " . PHP_VERSION . "</p>";

echo "<h2>1. Test PHP Basic</h2>";
echo "PHP functioneaza OK<br>";

echo "<h2>2. Test MySQL Extension</h2>";
if (extension_loaded('mysqli')) {
    echo "MySQLi extension: LOADED ✓<br>";
} else {
    echo "MySQLi extension: NOT LOADED ✗<br>";
}

echo "<h2>3. Test Database Connection</h2>";
// Incearca conexiune fara config (manual)
$conn = @new mysqli('localhost', '', '', '');
if ($conn->connect_error) {
    echo "Connection error (normal, asteptat): " . $conn->connect_error . "<br>";
} else {
    echo "MySQL server: ACCESIBIL ✓<br>";
    $conn->close();
}

echo "<h2>4. Test Config File</h2>";
if (file_exists('config/database.php')) {
    echo "config/database.php: EXISTS ✓<br>";
    require_once 'config/database.php';
    echo "config/database.php: LOADED ✓<br>";

    // Arata constantele (fara passwords)
    if (defined('DB_HOST')) echo "DB_HOST: " . DB_HOST . "<br>";
    if (defined('DB_USER')) echo "DB_USER: " . DB_USER . "<br>";
    if (defined('DB_NAME')) echo "DB_NAME: " . DB_NAME . "<br>";
} else {
    echo "config/database.php: NOT FOUND ✗<br>";
}

echo "<h2>5. Test Includes</h2>";
if (file_exists('includes/functions.php')) {
    echo "includes/functions.php: EXISTS ✓<br>";
} else {
    echo "includes/functions.php: NOT FOUND ✗<br>";
}

echo "<h2>6. Current Directory</h2>";
echo "Current dir: " . getcwd() . "<br>";

echo "<h2>7. Files in Current Directory</h2>";
$files = scandir('.');
echo "<pre>";
print_r($files);
echo "</pre>";

echo "<h2>Done!</h2>";
