<?php
/**
 * Verificare autentificare
 * Include acest fișier în toate paginile care necesită autentificare
 */

session_start();

// Verifică dacă utilizatorul este autentificat
if (!isset($_SESSION['user_id']) || !isset($_SESSION['username'])) {
    // Redirecționează către login
    header('Location: /login.php');
    exit;
}

// Verifică timeout sesiune (30 minute inactivitate)
$timeout = 1800; // 30 minute în secunde

if (isset($_SESSION['last_activity']) && (time() - $_SESSION['last_activity']) > $timeout) {
    // Sesiune expirată
    session_unset();
    session_destroy();
    header('Location: /login.php?timeout=1');
    exit;
}

// Actualizează timpul ultimei activități
$_SESSION['last_activity'] = time();
