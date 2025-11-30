<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once 'config/database.php';

echo "<h1>Verificare User Admin</h1>";

$conn = getDbConnection();
if (!$conn) die("Nu pot conecta la DB");

// Selectează user admin
$result = $conn->query("SELECT * FROM users WHERE username='admin'");

if ($result->num_rows > 0) {
    $user = $result->fetch_assoc();
    echo "<h2>User găsit:</h2>";
    echo "<p>ID: " . $user['id'] . "</p>";
    echo "<p>Username: " . $user['username'] . "</p>";
    echo "<p>Email: " . ($user['email'] ?? 'NULL') . "</p>";
    echo "<p>Password hash: " . $user['password'] . "</p>";

    echo "<h2>Test Password Verify:</h2>";

    // Test cu admin123
    if (password_verify('admin123', $user['password'])) {
        echo "<p style='color: green; font-size: 20px;'>✓ Password 'admin123' este CORECT!</p>";
    } else {
        echo "<p style='color: red; font-size: 20px;'>✗ Password 'admin123' NU funcționează!</p>";

        // Generăm un hash nou
        $new_hash = password_hash('admin123', PASSWORD_BCRYPT);
        echo "<p>Hash nou generat: " . $new_hash . "</p>";
        echo "<p>Rulează în phpMyAdmin:</p>";
        echo "<pre>UPDATE users SET password = '" . $new_hash . "' WHERE username = 'admin';</pre>";
    }
} else {
    echo "<p style='color: red;'>User 'admin' NU există!</p>";
}

$conn->close();
?>
