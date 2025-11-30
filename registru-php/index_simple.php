<?php
// Versiune simpla fara database - pentru a testa daca merge
error_reporting(E_ALL);
ini_set('display_errors', 1);
?>
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registru Import RE1 - Căutare Containere</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-navy">
        <div class="container-fluid">
            <a class="navbar-brand" href="index.php">
                <i class="bi bi-ship"></i> Registru Import RE1
            </a>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card shadow">
                    <div class="card-header bg-navy text-white">
                        <h4 class="mb-0"><i class="bi bi-search"></i> Căutare Container</h4>
                    </div>
                    <div class="card-body">
                        <form id="searchForm">
                            <div class="mb-3">
                                <label for="container_number" class="form-label">Număr Container</label>
                                <input type="text" class="form-control" id="container_number"
                                       placeholder="Ex: ABCD1234567" required>
                            </div>
                            <button type="submit" class="btn btn-navy w-100">
                                <i class="bi bi-search"></i> Căutare
                            </button>
                        </form>

                        <div id="results" class="mt-4"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="footer mt-5 py-3 bg-light">
        <div class="container text-center">
            <span class="text-muted">Registru Import RE1 - <?php echo date('Y'); ?></span>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('searchForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('results').innerHTML =
                '<div class="alert alert-info">Funcția de căutare necesită configurarea bazei de date.</div>';
        });
    </script>
</body>
</html>
