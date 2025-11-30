<?php
session_start();
require_once 'config/database.php';
require_once 'includes/functions.php';

// Dacă utilizatorul este deja autentificat, redirecționează
if (isset($_SESSION['user_id'])) {
    redirect('/admin.php');
}

$error = '';
$timeout_message = '';

// Verifică mesaj timeout
if (isset($_GET['timeout'])) {
    $timeout_message = 'Sesiunea a expirat din cauza inactivității. Te rugăm să te autentifici din nou.';
}

// Procesează formular login
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username'] ?? '');
    $password = trim($_POST['password'] ?? '');

    if (empty($username) || empty($password)) {
        $error = 'Te rugăm să completezi toate câmpurile.';
    } else {
        // Caută utilizatorul în baza de date
        $sql = "SELECT * FROM users WHERE username = ?";
        $user = dbFetchOne($sql, [$username]);

        if ($user && verifyPassword($password, $user['password'])) {
            // Autentificare reușită
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['username'] = $user['username'];
            $_SESSION['last_activity'] = time();

            // Actualizează last_login
            $updateSql = "UPDATE users SET last_login = NOW() WHERE id = ?";
            dbQuery($updateSql, [$user['id']]);

            // Redirecționează către admin
            redirect('/admin.php');
        } else {
            $error = 'Nume utilizator sau parolă incorectă.';
        }
    }
}
?>
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Autentificare - Registru Import RE1</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/assets/css/style.css">
    <style>
        body {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            max-width: 450px;
            width: 100%;
            padding: 20px;
        }
        .login-card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            padding: 40px;
        }
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .login-header h1 {
            color: #1e3c72;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .login-header p {
            color: #6c757d;
            font-size: 14px;
        }
        .btn-login {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            border: none;
            padding: 12px;
            font-size: 16px;
            font-weight: 500;
            width: 100%;
        }
        .btn-login:hover {
            background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-card">
            <div class="login-header">
                <h1>Registru Import RE1</h1>
                <p>Autentificare administrare</p>
            </div>

            <?php if ($timeout_message): ?>
                <div class="alert alert-warning alert-dismissible fade show" role="alert">
                    <?= sanitize($timeout_message) ?>
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            <?php endif; ?>

            <?php if ($error): ?>
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <?= sanitize($error) ?>
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            <?php endif; ?>

            <form method="POST" action="">
                <div class="mb-3">
                    <label for="username" class="form-label">Nume utilizator</label>
                    <input type="text" class="form-control" id="username" name="username"
                           value="<?= sanitize($_POST['username'] ?? '') ?>" required autofocus>
                </div>

                <div class="mb-4">
                    <label for="password" class="form-label">Parolă</label>
                    <input type="password" class="form-control" id="password" name="password" required>
                </div>

                <button type="submit" class="btn btn-primary btn-login">
                    Autentificare
                </button>
            </form>

            <div class="text-center mt-4">
                <a href="/index.php" class="text-muted" style="text-decoration: none; font-size: 14px;">
                    &larr; Înapoi la pagina principală
                </a>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
