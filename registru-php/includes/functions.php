<?php
/**
 * Funcții helper pentru aplicație
 */

/**
 * Returnează URL-ul complet către imagine container
 */
function getContainerImage($containerNumber) {
    if (empty($containerNumber) || strlen($containerNumber) < 4) {
        return '/images/containere/default.jpg';
    }

    // Extrage prefixul (primele 4 caractere, ex: GCXU, TRHU)
    $prefix = strtoupper(substr($containerNumber, 0, 4));

    // Determină tipul containerului
    $containerType = determineContainerType($containerNumber);

    // Calea către imagine
    $imagePath = "/images/containere/{$containerType}/{$prefix}.jpg";

    // Verifică dacă există imaginea
    if (file_exists($_SERVER['DOCUMENT_ROOT'] . $imagePath)) {
        return $imagePath;
    }

    // Încearcă extensii alternative
    $extensions = ['.png', '.jpeg', '.webp'];
    foreach ($extensions as $ext) {
        $altPath = "/images/containere/{$containerType}/{$prefix}{$ext}";
        if (file_exists($_SERVER['DOCUMENT_ROOT'] . $altPath)) {
            return $altPath;
        }
    }

    return "/images/containere/default.jpg";
}

/**
 * Determină tipul containerului din număr
 */
function determineContainerType($containerNumber) {
    // Logică de determinare bazată pe lungime sau alte reguli
    // Poți adapta în funcție de formatul real al numerelor

    $length = strlen($containerNumber);

    if ($length >= 11) {
        // Containere mai mari (45G1, 40G1)
        return '45G1';
    } elseif ($length >= 10) {
        return '40G1';
    } elseif ($length >= 9) {
        return '22G1';
    } else {
        return '20G1';
    }
}

/**
 * Returnează URL-ul către steag țară
 */
function getFlagImage($countryCode) {
    if (empty($countryCode)) {
        return '/images/drapele/default.png';
    }

    $code = strtoupper($countryCode);
    $imagePath = "/images/drapele/{$code}.png";

    if (file_exists($_SERVER['DOCUMENT_ROOT'] . $imagePath)) {
        return $imagePath;
    }

    return '/images/drapele/default.png';
}

/**
 * Returnează URL-ul către imagine navă
 */
function getShipImage($shipName) {
    if (empty($shipName)) {
        return '/images/nave/default.jpg';
    }

    // Normalizează numele navei pentru nume fișier
    $filename = strtolower(str_replace(' ', '_', $shipName));
    $imagePath = "/images/nave/{$filename}.jpg";

    if (file_exists($_SERVER['DOCUMENT_ROOT'] . $imagePath)) {
        return $imagePath;
    }

    return '/images/nave/default.jpg';
}

/**
 * Formatează data pentru afișare
 */
function formatDate($date, $format = 'd.m.Y') {
    if (empty($date)) {
        return '-';
    }

    $timestamp = strtotime($date);
    return date($format, $timestamp);
}

/**
 * Formatează greutatea
 */
function formatWeight($weight) {
    if (empty($weight)) {
        return '-';
    }

    return number_format($weight, 2, ',', '.') . ' kg';
}

/**
 * Sanitizează input pentru afișare HTML
 */
function sanitize($string) {
    return htmlspecialchars($string, ENT_QUOTES, 'UTF-8');
}

/**
 * Returnează mesaj success/error în format HTML
 */
function showMessage($message, $type = 'success') {
    $class = $type === 'success' ? 'alert-success' : 'alert-danger';
    return "<div class='alert {$class} alert-dismissible fade show' role='alert'>
                {$message}
                <button type='button' class='btn-close' data-bs-dismiss='alert'></button>
            </div>";
}

/**
 * Validează număr container (format ISO)
 */
function validateContainerNumber($number) {
    // Format: 4 litere + 6 cifre + 1 cifră de verificare
    // Ex: GCXU1234567

    if (strlen($number) !== 11) {
        return false;
    }

    // Primele 4 caractere trebuie să fie litere
    if (!ctype_alpha(substr($number, 0, 4))) {
        return false;
    }

    // Următoarele 7 caractere trebuie să fie cifre
    if (!ctype_digit(substr($number, 4, 7))) {
        return false;
    }

    return true;
}

/**
 * Generează hash pentru parolă
 */
function hashPassword($password) {
    return password_hash($password, PASSWORD_DEFAULT);
}

/**
 * Verifică parolă
 */
function verifyPassword($password, $hash) {
    return password_verify($password, $hash);
}

/**
 * Generează token CSRF
 */
function generateCSRFToken() {
    if (!isset($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

/**
 * Verifică token CSRF
 */
function verifyCSRFToken($token) {
    return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}

/**
 * Redirect către altă pagină
 */
function redirect($url) {
    header("Location: $url");
    exit;
}

/**
 * Verifică dacă request-ul este AJAX
 */
function isAjax() {
    return isset($_SERVER['HTTP_X_REQUESTED_WITH']) &&
           strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest';
}

/**
 * Returnează răspuns JSON
 */
function jsonResponse($data, $statusCode = 200) {
    http_response_code($statusCode);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

/**
 * Validează și sanitizează date Excel import
 */
function sanitizeExcelData($data) {
    $sanitized = [];

    foreach ($data as $key => $value) {
        // Curăță spații
        $value = trim($value);

        // Înlocuiește multiple spații cu unul singur
        $value = preg_replace('/\s+/', ' ', $value);

        $sanitized[$key] = $value;
    }

    return $sanitized;
}

/**
 * Paginare
 */
function paginate($totalItems, $itemsPerPage = 20, $currentPage = 1) {
    $totalPages = ceil($totalItems / $itemsPerPage);
    $currentPage = max(1, min($currentPage, $totalPages));

    $offset = ($currentPage - 1) * $itemsPerPage;

    return [
        'total_items' => $totalItems,
        'total_pages' => $totalPages,
        'current_page' => $currentPage,
        'items_per_page' => $itemsPerPage,
        'offset' => $offset,
        'has_prev' => $currentPage > 1,
        'has_next' => $currentPage < $totalPages
    ];
}
