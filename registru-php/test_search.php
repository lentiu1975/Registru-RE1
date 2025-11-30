<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

require_once 'config/database.php';

echo "<h1>Test Căutare Containere</h1>";

$conn = getDbConnection();
if (!$conn) die("Nu pot conecta la DB");

// Test 1: Câte containere avem?
$result = $conn->query("SELECT COUNT(*) as total FROM manifest_entries");
$row = $result->fetch_assoc();
echo "<h2>Total containere în DB: " . $row['total'] . "</h2>";

// Test 2: Primele 10 containere
echo "<h2>Primele 10 containere:</h2>";
$result = $conn->query("SELECT * FROM manifest_entries LIMIT 10");
echo "<table border='1' cellpadding='5'>";
echo "<tr><th>ID</th><th>Manifest ID</th><th>Container</th><th>Tip</th><th>Greutate</th></tr>";
while ($row = $result->fetch_assoc()) {
    echo "<tr>";
    echo "<td>" . $row['id'] . "</td>";
    echo "<td>" . $row['manifest_id'] . "</td>";
    echo "<td><strong>" . htmlspecialchars($row['container_number']) . "</strong></td>";
    echo "<td>" . htmlspecialchars($row['container_type']) . "</td>";
    echo "<td>" . $row['weight'] . "</td>";
    echo "</tr>";
}
echo "</table>";

// Test 3: Caută un container specific
$test_container = $conn->query("SELECT container_number FROM manifest_entries LIMIT 1")->fetch_assoc()['container_number'];
echo "<h2>Test căutare pentru: " . htmlspecialchars($test_container) . "</h2>";

$stmt = $conn->prepare("SELECT * FROM manifest_entries WHERE container_number LIKE ?");
$search = "%{$test_container}%";
$stmt->bind_param("s", $search);
$stmt->execute();
$result = $stmt->get_result();

echo "<p>Găsite: " . $result->num_rows . " rezultate</p>";
if ($result->num_rows > 0) {
    echo "<p style='color: green;'>✓ Căutarea funcționează!</p>";
} else {
    echo "<p style='color: red;'>✗ Căutarea NU funcționează!</p>";
}

$conn->close();
?>
