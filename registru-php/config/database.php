<?php
/**
 * Configurare conexiune MySQL
 * Modifică valorile pentru producție!
 */

// Configurare pentru localhost (development)
define('DB_HOST_LOCAL', 'localhost');
define('DB_USER_LOCAL', 'root');
define('DB_PASS_LOCAL', '');
define('DB_NAME_LOCAL', 'registru_import_re1');

// Configurare pentru producție (vamactasud.lentiu.ro)
define('DB_HOST_PROD', 'localhost');
define('DB_USER_PROD', 'lentiuro_vamauser');
define('DB_PASS_PROD', 'VamaCtaSud2025!');
define('DB_NAME_PROD', 'lentiuro_vamactasud');

// Detectare environment
$is_production = (isset($_SERVER['HTTP_HOST']) && strpos($_SERVER['HTTP_HOST'], 'vamactasud.lentiu.ro') !== false);

if ($is_production) {
    define('DB_HOST', DB_HOST_PROD);
    define('DB_USER', DB_USER_PROD);
    define('DB_PASS', DB_PASS_PROD);
    define('DB_NAME', DB_NAME_PROD);
} else {
    define('DB_HOST', DB_HOST_LOCAL);
    define('DB_USER', DB_USER_LOCAL);
    define('DB_PASS', DB_PASS_LOCAL);
    define('DB_NAME', DB_NAME_LOCAL);
}

/**
 * Creează conexiune MySQL
 */
function getDbConnection() {
    // Verifică dacă credențialele sunt configurate
    if (empty(DB_USER) || empty(DB_NAME)) {
        return null;  // Returnează null dacă nu e configurat
    }

    $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);

    if ($conn->connect_error) {
        return null;  // Returnează null în loc să crape
    }

    // Set charset UTF-8
    $conn->set_charset("utf8mb4");

    return $conn;
}

/**
 * Execută query și returnează rezultat
 */
function dbQuery($sql, $params = []) {
    $conn = getDbConnection();

    if ($conn === null) {
        return false;  // Database nu e configurat
    }

    if (!empty($params)) {
        $stmt = $conn->prepare($sql);
        if ($stmt === false) {
            $conn->close();
            return false;
        }

        // Bind parameters
        $types = str_repeat('s', count($params));
        $stmt->bind_param($types, ...$params);
        $stmt->execute();
        $result = $stmt->get_result();
        $stmt->close();
    } else {
        $result = $conn->query($sql);
    }

    $conn->close();
    return $result;
}

/**
 * Returnează o singură linie
 */
function dbFetchOne($sql, $params = []) {
    $result = dbQuery($sql, $params);
    if ($result === false) {
        return null;
    }
    $row = $result->fetch_assoc();
    return $row;
}

/**
 * Returnează toate liniile
 */
function dbFetchAll($sql, $params = []) {
    $result = dbQuery($sql, $params);
    if ($result === false) {
        return [];
    }
    $rows = [];
    while ($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }
    return $rows;
}

/**
 * Verifică dacă baza de date este configurată
 */
function isDatabaseConfigured() {
    return !empty(DB_USER) && !empty(DB_NAME);
}
