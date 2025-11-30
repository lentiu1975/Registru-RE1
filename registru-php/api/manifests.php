<?php
/**
 * API pentru gestionare manifeste
 * Suportă: GET, POST, PUT, DELETE
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

session_start();
require_once '../config/database.php';
require_once '../includes/functions.php';

$method = $_SERVER['REQUEST_METHOD'];

// Doar GET este public, restul necesită autentificare
if ($method !== 'GET') {
    if (!isset($_SESSION['user_id'])) {
        jsonResponse(['error' => 'Autentificare necesară'], 401);
    }
}

switch ($method) {
    case 'GET':
        handleGet();
        break;
    case 'POST':
        handlePost();
        break;
    case 'PUT':
        handlePut();
        break;
    case 'DELETE':
        handleDelete();
        break;
    default:
        jsonResponse(['error' => 'Metodă nepermisă'], 405);
}

/**
 * GET - Listare manifeste sau detalii manifest specific
 */
function handleGet() {
    // Verifică dacă se cere un manifest specific
    $manifestId = $_GET['id'] ?? null;

    if ($manifestId) {
        // Returnează manifest specific cu intrări
        $manifest = getManifestById($manifestId);
        if (!$manifest) {
            jsonResponse(['error' => 'Manifest negăsit'], 404);
        }
        jsonResponse($manifest);
    } else {
        // Returnează lista de manifeste cu paginare
        $page = max(1, intval($_GET['page'] ?? 1));
        $perPage = min(100, max(10, intval($_GET['per_page'] ?? 20)));
        $search = $_GET['search'] ?? '';

        $manifests = getManifests($page, $perPage, $search);
        jsonResponse($manifests);
    }
}

/**
 * POST - Creare manifest nou
 */
function handlePost() {
    $data = json_decode(file_get_contents('php://input'), true);

    if (!$data) {
        jsonResponse(['error' => 'Date invalide'], 400);
    }

    // Validare
    $required = ['manifest_number', 'arrival_date'];
    foreach ($required as $field) {
        if (empty($data[$field])) {
            jsonResponse(['error' => "Câmpul '$field' este obligatoriu"], 400);
        }
    }

    // Verifică dacă manifestul există deja
    $existing = dbFetchOne("SELECT id FROM manifests WHERE manifest_number = ?", [$data['manifest_number']]);
    if ($existing) {
        jsonResponse(['error' => 'Manifestul există deja'], 409);
    }

    // Gestionează nava
    $shipId = null;
    if (!empty($data['ship_name'])) {
        $ship = dbFetchOne("SELECT id FROM ships WHERE name = ?", [$data['ship_name']]);
        if (!$ship) {
            // Creează navă nouă
            dbQuery("INSERT INTO ships (name) VALUES (?)", [$data['ship_name']]);
            $conn = getDbConnection();
            $shipId = $conn->insert_id;
            $conn->close();
        } else {
            $shipId = $ship['id'];
        }
    }

    // Gestionează portul
    $portId = null;
    if (!empty($data['port_name'])) {
        $port = dbFetchOne("SELECT id FROM ports WHERE name = ?", [$data['port_name']]);
        if (!$port) {
            dbQuery("INSERT INTO ports (name) VALUES (?)", [$data['port_name']]);
            $conn = getDbConnection();
            $portId = $conn->insert_id;
            $conn->close();
        } else {
            $portId = $port['id'];
        }
    }

    // Inserează manifest
    $sql = "INSERT INTO manifests (manifest_number, ship_id, arrival_date, port_id) VALUES (?, ?, ?, ?)";
    dbQuery($sql, [$data['manifest_number'], $shipId, $data['arrival_date'], $portId]);

    $conn = getDbConnection();
    $manifestId = $conn->insert_id;
    $conn->close();

    // Returnează manifestul creat
    $manifest = getManifestById($manifestId);
    jsonResponse($manifest, 201);
}

/**
 * PUT - Actualizare manifest
 */
function handlePut() {
    $data = json_decode(file_get_contents('php://input'), true);

    if (!$data || empty($data['id'])) {
        jsonResponse(['error' => 'Date invalide'], 400);
    }

    $manifestId = $data['id'];

    // Verifică dacă manifestul există
    $existing = dbFetchOne("SELECT id FROM manifests WHERE id = ?", [$manifestId]);
    if (!$existing) {
        jsonResponse(['error' => 'Manifest negăsit'], 404);
    }

    // Construiește query update dinamic
    $updates = [];
    $params = [];

    if (isset($data['manifest_number'])) {
        $updates[] = "manifest_number = ?";
        $params[] = $data['manifest_number'];
    }

    if (isset($data['arrival_date'])) {
        $updates[] = "arrival_date = ?";
        $params[] = $data['arrival_date'];
    }

    if (isset($data['ship_name'])) {
        $ship = dbFetchOne("SELECT id FROM ships WHERE name = ?", [$data['ship_name']]);
        if (!$ship) {
            dbQuery("INSERT INTO ships (name) VALUES (?)", [$data['ship_name']]);
            $conn = getDbConnection();
            $shipId = $conn->insert_id;
            $conn->close();
        } else {
            $shipId = $ship['id'];
        }
        $updates[] = "ship_id = ?";
        $params[] = $shipId;
    }

    if (empty($updates)) {
        jsonResponse(['error' => 'Nicio modificare specificată'], 400);
    }

    $params[] = $manifestId;
    $sql = "UPDATE manifests SET " . implode(', ', $updates) . " WHERE id = ?";
    dbQuery($sql, $params);

    $manifest = getManifestById($manifestId);
    jsonResponse($manifest);
}

/**
 * DELETE - Ștergere manifest
 */
function handleDelete() {
    $manifestId = $_GET['id'] ?? null;

    if (!$manifestId) {
        jsonResponse(['error' => 'ID manifest lipsă'], 400);
    }

    // Verifică dacă manifestul există
    $existing = dbFetchOne("SELECT id FROM manifests WHERE id = ?", [$manifestId]);
    if (!$existing) {
        jsonResponse(['error' => 'Manifest negăsit'], 404);
    }

    // Șterge manifestul (și intrările prin CASCADE)
    dbQuery("DELETE FROM manifests WHERE id = ?", [$manifestId]);

    jsonResponse(['success' => true, 'message' => 'Manifest șters cu succes']);
}

/**
 * Helper: Obține manifest după ID cu toate intrările
 */
function getManifestById($id) {
    $sql = "SELECT m.*, s.name as ship_name, p.name as port_name
            FROM manifests m
            LEFT JOIN ships s ON m.ship_id = s.id
            LEFT JOIN ports p ON m.port_id = p.id
            WHERE m.id = ?";

    $manifest = dbFetchOne($sql, [$id]);

    if (!$manifest) {
        return null;
    }

    // Obține intrările
    $entriesSql = "SELECT me.*, c.name as country_name, c.flag_image
                   FROM manifest_entries me
                   LEFT JOIN countries c ON me.country_code = c.code
                   WHERE me.manifest_id = ?
                   ORDER BY me.id ASC";

    $entries = dbFetchAll($entriesSql, [$id]);

    // Adaugă imagini pentru fiecare intrare
    foreach ($entries as &$entry) {
        $entry['container_image'] = getContainerImage($entry['container_number']);
        $entry['flag_image'] = getFlagImage($entry['country_code']);
    }

    $manifest['entries'] = $entries;
    $manifest['entries_count'] = count($entries);

    return $manifest;
}

/**
 * Helper: Obține lista de manifeste cu paginare
 */
function getManifests($page, $perPage, $search) {
    // Count total
    $countSql = "SELECT COUNT(*) as total FROM manifests m WHERE 1=1";
    $params = [];

    if ($search) {
        $countSql .= " AND (m.manifest_number LIKE ? OR EXISTS (
            SELECT 1 FROM ships s WHERE s.id = m.ship_id AND s.name LIKE ?
        ))";
        $searchParam = "%{$search}%";
        $params = [$searchParam, $searchParam];
    }

    $countResult = dbFetchOne($countSql, $params);
    $total = $countResult['total'];

    // Calculează paginare
    $pagination = paginate($total, $perPage, $page);

    // Query pentru manifeste
    $sql = "SELECT m.*, s.name as ship_name, p.name as port_name,
            (SELECT COUNT(*) FROM manifest_entries WHERE manifest_id = m.id) as entries_count
            FROM manifests m
            LEFT JOIN ships s ON m.ship_id = s.id
            LEFT JOIN ports p ON m.port_id = p.id
            WHERE 1=1";

    if ($search) {
        $sql .= " AND (m.manifest_number LIKE ? OR s.name LIKE ?)";
    }

    $sql .= " ORDER BY m.arrival_date DESC, m.id DESC LIMIT ? OFFSET ?";

    $params[] = $perPage;
    $params[] = $pagination['offset'];

    $manifests = dbFetchAll($sql, $params);

    return [
        'data' => $manifests,
        'pagination' => $pagination
    ];
}
