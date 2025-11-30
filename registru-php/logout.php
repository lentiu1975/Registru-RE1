<?php
session_start();

// Distruge toate datele sesiunii
$_SESSION = array();

// Distruge cookie-ul sesiunii
if (isset($_COOKIE[session_name()])) {
    setcookie(session_name(), '', time() - 42000, '/');
}

// Distruge sesiunea
session_destroy();

// Redirecționează către login
header('Location: /login.php');
exit;
