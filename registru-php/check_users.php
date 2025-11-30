<?php
// Script de debug pentru verificare useri
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once 'config/database.php';

echo "<h1>DEBUG - Verificare Useri</h1>";

$conn = getDbConnection();

if ($conn === null) {
    die("ERROR: Nu pot conecta la database!");
}

echo "<p>✓ Conexiune OK la database</p>";

// Verifică câți useri există
$result = $conn->query("SELECT COUNT(*) as total FROM users");
$row = $result->fetch_assoc();
echo "<p>Total useri în database: " . $row['total'] . "</p>";

// Listează toți userii
$result = $conn->query("SELECT id, username, email, role, created_at FROM users");

echo "<h2>Useri în baza de date:</h2>";
echo "<table border='1' cellpadding='5'>";
echo "<tr><th>ID</th><th>Username</th><th>Email</th><th>Role</th><th>Created At</th></tr>";

while ($user = $result->fetch_assoc()) {
    echo "<tr>";
    echo "<td>" . $user['id'] . "</td>";
    echo "<td>" . $user['username'] . "</td>";
    echo "<td>" . $user['email'] . "</td>";
    echo "<td>" . $user['role'] . "</td>";
    echo "<td>" . $user['created_at'] . "</td>";
    echo "</tr>";
}

echo "</table>";

// Test password hash
echo "<h2>Test Password Hash:</h2>";
$test_password = 'admin123';
$test_hash = password_hash($test_password, PASSWORD_BCRYPT);
echo "<p>Password: admin123</p>";
echo "<p>Hash generat acum: " . $test_hash . "</p>";

// Verifică hash-ul din database
$result = $conn->query("SELECT password FROM users WHERE username='admin'");
if ($result && $result->num_rows > 0) {
    $user = $result->fetch_assoc();
    echo "<p>Hash din database: " . $user['password'] . "</p>";

    // Test verify
    if (password_verify('admin123', $user['password'])) {
        echo "<p style='color: green;'>✓ Password verify: OK! Hash-ul e valid pentru 'admin123'</p>";
    } else {
        echo "<p style='color: red;'>✗ Password verify: FAIL! Hash-ul NU e valid pentru 'admin123'</p>";
        echo "<p>Trebuie resetat password-ul!</p>";
    }
} else {
    echo "<p style='color: red;'>Nu există user 'admin' în database!</p>";
}

$conn->close();
?>
