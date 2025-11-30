<?php
require_once 'config/database.php';

$conn = getDbConnection();
$result = $conn->query("DESCRIBE manifest_entries");

echo "Coloane în manifest_entries:\n";
while ($row = $result->fetch_assoc()) {
    echo "- " . $row['Field'] . " (" . $row['Type'] . ")\n";
}

echo "\n\nColoane în manifests:\n";
$result = $conn->query("DESCRIBE manifests");
while ($row = $result->fetch_assoc()) {
    echo "- " . $row['Field'] . " (" . $row['Type'] . ")\n";
}
