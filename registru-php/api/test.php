<?php
// Test minimal pentru debug
error_reporting(E_ALL);
ini_set('display_errors', 1);

header('Content-Type: application/json; charset=utf-8');

try {
    require_once '../config/database.php';
    require_once '../includes/functions.php';

    $query = "SUDU";
    $searchParam = "%{$query}%";

    $sql = "SELECT me.*, m.manifest_number, m.arrival_date
            FROM manifest_entries me
            LEFT JOIN manifests m ON me.manifest_id = m.id
            WHERE me.container_number LIKE ?
            LIMIT 5";

    $results = dbFetchAll($sql, [$searchParam]);

    echo json_encode([
        'success' => true,
        'count' => count($results),
        'results' => $results
    ], JSON_PRETTY_PRINT);

} catch (Exception $e) {
    echo json_encode([
        'error' => $e->getMessage(),
        'file' => $e->getFile(),
        'line' => $e->getLine(),
        'trace' => $e->getTraceAsString()
    ], JSON_PRETTY_PRINT);
}
