<?php
/**
 * API pentru căutare containere
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');

require_once '../config/database.php';
require_once '../includes/functions.php';

$query = trim($_GET['q'] ?? '');

if (empty($query)) {
    jsonResponse(['error' => 'Query de căutare lipsă'], 400);
}

// Căutare simpla fara JOIN cu ships (ship_id nu e populat in manifests)
$sql = "SELECT me.*, m.manifest_number, m.arrival_date
        FROM manifest_entries me
        LEFT JOIN manifests m ON me.manifest_id = m.id
        WHERE me.container_number LIKE ?
           OR COALESCE(me.goods_description, '') LIKE ?
           OR COALESCE(m.manifest_number, '') LIKE ?
        ORDER BY me.id DESC
        LIMIT 100";

$searchParam = "%{$query}%";
$params = [$searchParam, $searchParam, $searchParam];

$results = dbFetchAll($sql, $params);

// Procesează fiecare rezultat
foreach ($results as &$result) {
    // Container image bazat pe prefixul din container_number
    $containerNumber = $result['container_number'] ?? '';
    $containerType = $result['container_type'] ?? '45G1';
    $prefix = substr($containerNumber, 0, 4); // Ex: CAAU din CAAU8601408

    // Caută imagine container: /Containere/{type}/{prefix}.jpg
    $containerImagePath = "/Containere/{$containerType}/{$prefix}.jpg";
    if (file_exists($_SERVER['DOCUMENT_ROOT'] . $containerImagePath)) {
        $result['container_image'] = $containerImagePath;
    } else {
        // Fallback la imagine generică: /Containere/{type}.jpg
        $genericPath = "/Containere/{$containerType}.jpg";
        if (file_exists($_SERVER['DOCUMENT_ROOT'] . $genericPath)) {
            $result['container_image'] = $genericPath;
        } else {
            // Fallback final
            $result['container_image'] = '/Containere/Container.png';
        }
    }

    // Nu avem ship_name in rezultate - vom seta null
    $result['ship_name'] = null;
    $result['ship_image'] = null;
    $result['flag_image'] = null;
}

jsonResponse([
    'query' => $query,
    'count' => count($results),
    'results' => $results
]);
