<?php
/**
 * API pentru import Excel
 * Suportă .xls și .xlsx
 */

session_start();
require_once '../config/database.php';
require_once '../includes/functions.php';

// Verifică autentificare
if (!isset($_SESSION['user_id'])) {
    jsonResponse(['error' => 'Autentificare necesară'], 401);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    jsonResponse(['error' => 'Metodă nepermisă'], 405);
}

// Verifică dacă fișierul a fost încărcat
if (!isset($_FILES['file']) || $_FILES['file']['error'] !== UPLOAD_ERR_OK) {
    $error = $_FILES['file']['error'] ?? 'necunoscut';
    jsonResponse(['error' => "Eroare upload fișier: {$error}"], 400);
}

$file = $_FILES['file'];
$filename = $file['name'];
$tmpPath = $file['tmp_name'];

// Verifică extensia
$ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
if (!in_array($ext, ['xls', 'xlsx'])) {
    jsonResponse(['error' => 'Doar fișiere .xls și .xlsx sunt permise'], 400);
}

// Mută fișierul în directorul uploads
$uploadDir = '../uploads/';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0755, true);
}

$newFilename = date('Y-m-d_His') . '_' . $filename;
$uploadPath = $uploadDir . $newFilename;

if (!move_uploaded_file($tmpPath, $uploadPath)) {
    jsonResponse(['error' => 'Eroare la salvarea fișierului'], 500);
}

// Procesează Excel
try {
    require_once '../vendor/autoload.php'; // PhpSpreadsheet

    $spreadsheet = \PhpOffice\PhpSpreadsheet\IOFactory::load($uploadPath);
    $sheet = $spreadsheet->getActiveSheet();
    $rows = $sheet->toArray();

    // Prima linie = header
    $header = array_shift($rows);

    // Mapare coloane (ajustează în funcție de structura Excel)
    $columnMap = detectColumnMapping($header);

    if (!$columnMap) {
        jsonResponse(['error' => 'Structura Excel nerecunoscută. Header: ' . implode(', ', $header)], 400);
    }

    // Procesează date
    $imported = 0;
    $failed = 0;
    $errors = [];

    // Inițiază tranzacție
    $conn = getDbConnection();
    $conn->begin_transaction();

    try {
        foreach ($rows as $index => $row) {
            $rowNum = $index + 2; // +2 pentru că index începe de la 0 și prima linie e header

            // Sare peste linii goale
            if (empty(array_filter($row))) {
                continue;
            }

            $data = sanitizeExcelData(mapRowToData($row, $columnMap));

            // Validare date minime
            if (empty($data['manifest_number']) || empty($data['container_number'])) {
                $errors[] = "Linia {$rowNum}: Lipsă număr manifest sau container";
                $failed++;
                continue;
            }

            // Găsește sau creează manifestul
            $manifestId = getOrCreateManifest($conn, $data);

            // Inserează intrarea
            $stmt = $conn->prepare("
                INSERT INTO manifest_entries
                (manifest_id, container_number, container_type, seal_number,
                 goods_description, weight, shipper, consignee, marks_numbers,
                 country_of_origin, country_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ");

            $stmt->bind_param('issssdsssss',
                $manifestId,
                $data['container_number'],
                $data['container_type'],
                $data['seal_number'],
                $data['goods_description'],
                $data['weight'],
                $data['shipper'],
                $data['consignee'],
                $data['marks_numbers'],
                $data['country_of_origin'],
                $data['country_code']
            );

            if ($stmt->execute()) {
                $imported++;
            } else {
                $errors[] = "Linia {$rowNum}: " . $stmt->error;
                $failed++;
            }

            $stmt->close();
        }

        // Commit tranzacție
        $conn->commit();

        // Log import
        $status = $failed > 0 ? 'partial' : 'success';
        $errorMsg = !empty($errors) ? implode("\n", $errors) : null;

        $logStmt = $conn->prepare("
            INSERT INTO import_logs (filename, rows_imported, rows_failed, status, error_message)
            VALUES (?, ?, ?, ?, ?)
        ");
        $logStmt->bind_param('siiss', $newFilename, $imported, $failed, $status, $errorMsg);
        $logStmt->execute();
        $logStmt->close();

        $conn->close();

        jsonResponse([
            'success' => true,
            'imported' => $imported,
            'failed' => $failed,
            'total' => $imported + $failed,
            'errors' => $errors,
            'filename' => $newFilename
        ]);

    } catch (Exception $e) {
        $conn->rollback();
        $conn->close();
        throw $e;
    }

} catch (Exception $e) {
    // Șterge fișierul uploadat
    if (file_exists($uploadPath)) {
        unlink($uploadPath);
    }

    jsonResponse(['error' => 'Eroare procesare Excel: ' . $e->getMessage()], 500);
}

/**
 * Detectează maparea coloanelor din header
 */
function detectColumnMapping($header) {
    // Normalizează header
    $normalized = array_map(function($h) {
        return strtolower(trim($h));
    }, $header);

    $map = [];

    // Caută coloane comune
    $mappings = [
        'manifest_number' => ['manifest', 'nr manifest', 'manifest number', 'manifest_number'],
        'container_number' => ['container', 'nr container', 'container number', 'container_number'],
        'container_type' => ['tip', 'type', 'container type', 'container_type'],
        'seal_number' => ['seal', 'sigiliu', 'seal number', 'seal_number'],
        'goods_description' => ['goods', 'marfa', 'description', 'goods_description'],
        'weight' => ['weight', 'greutate', 'kg'],
        'shipper' => ['shipper', 'expeditor'],
        'consignee' => ['consignee', 'destinatar'],
        'marks_numbers' => ['marks', 'marci', 'marks and numbers'],
        'country_of_origin' => ['country', 'tara', 'origin', 'country of origin'],
        'country_code' => ['code', 'cod tara', 'country code'],
        'arrival_date' => ['date', 'data', 'arrival', 'arrival date'],
        'ship_name' => ['ship', 'nava', 'vessel']
    ];

    foreach ($mappings as $field => $aliases) {
        foreach ($aliases as $alias) {
            $index = array_search($alias, $normalized);
            if ($index !== false) {
                $map[$field] = $index;
                break;
            }
        }
    }

    // Verifică dacă am găsit cel puțin coloanele esențiale
    if (!isset($map['manifest_number']) && !isset($map['container_number'])) {
        return null;
    }

    return $map;
}

/**
 * Mapează o linie la structura de date
 */
function mapRowToData($row, $columnMap) {
    $data = [];

    foreach ($columnMap as $field => $index) {
        $data[$field] = $row[$index] ?? null;
    }

    return $data;
}

/**
 * Găsește sau creează manifest
 */
function getOrCreateManifest($conn, $data) {
    $manifestNumber = $data['manifest_number'];

    // Caută manifest existent
    $stmt = $conn->prepare("SELECT id FROM manifests WHERE manifest_number = ?");
    $stmt->bind_param('s', $manifestNumber);
    $stmt->execute();
    $result = $stmt->get_result();
    $manifest = $result->fetch_assoc();
    $stmt->close();

    if ($manifest) {
        return $manifest['id'];
    }

    // Creează manifest nou
    $shipId = null;
    $portId = null;
    $arrivalDate = $data['arrival_date'] ?? date('Y-m-d');

    // Normalizează data
    if ($arrivalDate && !preg_match('/^\d{4}-\d{2}-\d{2}$/', $arrivalDate)) {
        $timestamp = strtotime($arrivalDate);
        if ($timestamp) {
            $arrivalDate = date('Y-m-d', $timestamp);
        } else {
            $arrivalDate = date('Y-m-d');
        }
    }

    // Găsește sau creează nava
    if (!empty($data['ship_name'])) {
        $stmt = $conn->prepare("SELECT id FROM ships WHERE name = ?");
        $stmt->bind_param('s', $data['ship_name']);
        $stmt->execute();
        $result = $stmt->get_result();
        $ship = $result->fetch_assoc();
        $stmt->close();

        if ($ship) {
            $shipId = $ship['id'];
        } else {
            $stmt = $conn->prepare("INSERT INTO ships (name) VALUES (?)");
            $stmt->bind_param('s', $data['ship_name']);
            $stmt->execute();
            $shipId = $conn->insert_id;
            $stmt->close();
        }
    }

    // Inserează manifestul
    $stmt = $conn->prepare("INSERT INTO manifests (manifest_number, ship_id, arrival_date, port_id) VALUES (?, ?, ?, ?)");
    $stmt->bind_param('sisi', $manifestNumber, $shipId, $arrivalDate, $portId);
    $stmt->execute();
    $manifestId = $conn->insert_id;
    $stmt->close();

    return $manifestId;
}
