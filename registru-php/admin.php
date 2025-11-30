<?php
require_once 'includes/auth.php';
require_once 'config/database.php';
require_once 'includes/functions.php';

// Obține statistici
$stats = [
    'total_manifests' => 0,
    'total_containers' => 0,
    'total_ships' => 0,
    'recent_imports' => 0
];

$statsResult = dbFetchOne("SELECT COUNT(*) as count FROM manifests");
$stats['total_manifests'] = $statsResult['count'];

$statsResult = dbFetchOne("SELECT COUNT(*) as count FROM manifest_entries");
$stats['total_containers'] = $statsResult['count'];

$statsResult = dbFetchOne("SELECT COUNT(*) as count FROM ships");
$stats['total_ships'] = $statsResult['count'];

$statsResult = dbFetchOne("SELECT COUNT(*) as count FROM import_logs WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)");
$stats['recent_imports'] = $statsResult['count'];
?>
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administrare - Registru Import RE1</title>

    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">

    <!-- Custom CSS -->
    <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-custom">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="bi bi-ship me-2"></i>
                Registru Import RE1
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">
                            <i class="bi bi-search me-1"></i>
                            Căutare
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="/admin.php">
                            <i class="bi bi-gear me-1"></i>
                            Administrare
                        </a>
                    </li>
                    <li class="nav-item">
                        <span class="nav-link text-light">
                            <i class="bi bi-person-circle me-1"></i>
                            <?= sanitize($_SESSION['username']) ?>
                        </span>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/logout.php">
                            <i class="bi bi-box-arrow-right me-1"></i>
                            Deconectare
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Header -->
    <div class="py-4" style="background: linear-gradient(135deg, var(--navy-primary) 0%, var(--navy-secondary) 100%);">
        <div class="container-fluid">
            <h1 class="text-white mb-0">
                <i class="bi bi-speedometer2 me-2"></i>
                Panou de Administrare
            </h1>
        </div>
    </div>

    <!-- Main Content -->
    <div class="container-fluid py-4">
        <!-- Statistics Cards -->
        <div class="row g-4 mb-4">
            <div class="col-md-3">
                <div class="stats-card">
                    <div class="stats-number"><?= number_format($stats['total_manifests']) ?></div>
                    <div class="stats-label">
                        <i class="bi bi-file-earmark-text me-1"></i>
                        Manifeste Totale
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card" style="border-left-color: var(--ocean-accent);">
                    <div class="stats-number"><?= number_format($stats['total_containers']) ?></div>
                    <div class="stats-label">
                        <i class="bi bi-box-seam me-1"></i>
                        Containere Totale
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card" style="border-left-color: var(--success-color);">
                    <div class="stats-number"><?= number_format($stats['total_ships']) ?></div>
                    <div class="stats-label">
                        <i class="bi bi-ship me-1"></i>
                        Nave Înregistrate
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stats-card" style="border-left-color: var(--warning-color);">
                    <div class="stats-number"><?= number_format($stats['recent_imports']) ?></div>
                    <div class="stats-label">
                        <i class="bi bi-upload me-1"></i>
                        Import-uri (7 zile)
                    </div>
                </div>
            </div>
        </div>

        <!-- Action Tabs -->
        <ul class="nav nav-tabs mb-4" id="adminTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="manifests-tab" data-bs-toggle="tab"
                        data-bs-target="#manifests" type="button">
                    <i class="bi bi-file-earmark-text me-1"></i>
                    Manifeste
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="import-tab" data-bs-toggle="tab"
                        data-bs-target="#import" type="button">
                    <i class="bi bi-cloud-upload me-1"></i>
                    Import Excel
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="logs-tab" data-bs-toggle="tab"
                        data-bs-target="#logs" type="button">
                    <i class="bi bi-clock-history me-1"></i>
                    Istoric Import
                </button>
            </li>
        </ul>

        <div class="tab-content" id="adminTabsContent">
            <!-- Manifests Tab -->
            <div class="tab-pane fade show active" id="manifests" role="tabpanel">
                <div class="card-custom">
                    <div class="card-header-custom">
                        <i class="bi bi-file-earmark-text me-2"></i>
                        Lista Manifeste
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-custom mb-0" id="manifestTable">
                                <thead>
                                    <tr>
                                        <th>Număr Manifest</th>
                                        <th>Navă</th>
                                        <th>Port</th>
                                        <th>Data Sosire</th>
                                        <th>Containere</th>
                                        <th>Acțiuni</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td colspan="6" class="text-center py-4">
                                            <div class="spinner-border spinner-navy" role="status">
                                                <span class="visually-hidden">Se încarcă...</span>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Pagination -->
                <div id="pagination" class="mt-4"></div>
            </div>

            <!-- Import Tab -->
            <div class="tab-pane fade" id="import" role="tabpanel">
                <div class="row">
                    <div class="col-lg-8 mx-auto">
                        <div class="card-custom">
                            <div class="card-header-custom">
                                <i class="bi bi-cloud-upload me-2"></i>
                                Import Fișier Excel
                            </div>
                            <div class="card-body p-4">
                                <form id="uploadForm" enctype="multipart/form-data">
                                    <div class="upload-area mb-4" onclick="document.getElementById('excelFile').click()">
                                        <i class="bi bi-cloud-upload" style="font-size: 3rem; color: var(--ocean-light);"></i>
                                        <h5 class="mt-3">Selectați fișier Excel</h5>
                                        <p class="text-muted mb-0">
                                            Faceți clic sau trageți fișierul aici
                                            <br>
                                            <small>Formate acceptate: .xls, .xlsx</small>
                                        </p>
                                        <input type="file"
                                               id="excelFile"
                                               name="file"
                                               accept=".xls,.xlsx"
                                               class="d-none"
                                               required>
                                    </div>

                                    <div id="fileName" class="mb-3 text-center"></div>

                                    <div class="text-center">
                                        <button type="submit" class="btn btn-navy btn-lg">
                                            <i class="bi bi-upload me-2"></i>
                                            Încarcă și Procesează
                                        </button>
                                    </div>
                                </form>

                                <!-- Upload Progress -->
                                <div id="uploadProgress" class="mt-4" style="display: none;">
                                    <div class="text-center">
                                        <div class="spinner-border spinner-navy mb-2" role="status"></div>
                                        <p class="text-muted">Se procesează fișierul...</p>
                                    </div>
                                </div>

                                <!-- Upload Results -->
                                <div id="uploadResults" class="mt-4"></div>

                                <!-- Instructions -->
                                <div class="alert alert-navy mt-4">
                                    <h6 class="fw-bold">
                                        <i class="bi bi-info-circle me-2"></i>
                                        Instrucțiuni Import Excel
                                    </h6>
                                    <ul class="mb-0 mt-2">
                                        <li>Fișierul trebuie să aibă un header în prima linie</li>
                                        <li>Coloane recunoscute: Manifest, Container, Tip, Seal, Goods, Weight, Shipper, Consignee, Country, Date, Ship</li>
                                        <li>Manifestele noi vor fi create automat</li>
                                        <li>Navele noi vor fi create automat</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Logs Tab -->
            <div class="tab-pane fade" id="logs" role="tabpanel">
                <div class="card-custom">
                    <div class="card-header-custom">
                        <i class="bi bi-clock-history me-2"></i>
                        Istoric Import-uri
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-custom mb-0">
                                <thead>
                                    <tr>
                                        <th>Fișier</th>
                                        <th>Importate</th>
                                        <th>Erori</th>
                                        <th>Status</th>
                                        <th>Data</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php
                                    $logs = dbFetchAll("SELECT * FROM import_logs ORDER BY created_at DESC LIMIT 50");

                                    if (empty($logs)) {
                                        echo '<tr><td colspan="5" class="text-center text-muted py-4">Nu există import-uri înregistrate</td></tr>';
                                    } else {
                                        foreach ($logs as $log) {
                                            $statusBadge = $log['status'] === 'success' ? 'badge-navy' :
                                                          ($log['status'] === 'partial' ? 'bg-warning' : 'bg-danger');
                                            $statusText = $log['status'] === 'success' ? 'Succes' :
                                                         ($log['status'] === 'partial' ? 'Parțial' : 'Eșuat');

                                            echo '<tr>';
                                            echo '<td>' . sanitize($log['filename']) . '</td>';
                                            echo '<td><span class="badge bg-success">' . $log['rows_imported'] . '</span></td>';
                                            echo '<td><span class="badge bg-danger">' . $log['rows_failed'] . '</span></td>';
                                            echo '<td><span class="badge ' . $statusBadge . '">' . $statusText . '</span></td>';
                                            echo '<td>' . formatDate($log['created_at'], 'd.m.Y H:i:s') . '</td>';
                                            echo '</tr>';

                                            if ($log['error_message']) {
                                                echo '<tr><td colspan="5" class="bg-light"><small class="text-danger">' . nl2br(sanitize($log['error_message'])) . '</small></td></tr>';
                                            }
                                        }
                                    }
                                    ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Manifest Details Modal -->
    <div class="modal fade" id="manifestModal" tabindex="-1">
        <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header modal-header-custom">
                    <h5 class="modal-title">
                        <i class="bi bi-file-earmark-text me-2"></i>
                        Detalii Manifest
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="manifestModalBody">
                    <!-- Content loaded via JavaScript -->
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="footer-custom">
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-6 text-center text-md-start">
                    <p class="mb-0">
                        &copy; <?= date('Y') ?> Registru Import RE1. Toate drepturile rezervate.
                    </p>
                </div>
                <div class="col-md-6 text-center text-md-end">
                    <p class="mb-0">
                        Powered by <a href="https://vama.lentiu.ro">Vama Lentiu</a>
                    </p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <!-- Custom JS -->
    <script src="/assets/js/app.js"></script>

    <!-- Additional Admin Scripts -->
    <script>
        // File input handler
        document.getElementById('excelFile')?.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                document.getElementById('fileName').innerHTML = `
                    <div class="alert alert-info">
                        <i class="bi bi-file-earmark-excel me-2"></i>
                        <strong>Fișier selectat:</strong> ${fileName}
                    </div>
                `;
            }
        });

        // Drag and drop
        const uploadArea = document.querySelector('.upload-area');
        if (uploadArea) {
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, preventDefaults, false);
            });

            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }

            ['dragenter', 'dragover'].forEach(eventName => {
                uploadArea.addEventListener(eventName, () => {
                    uploadArea.classList.add('drag-over');
                }, false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, () => {
                    uploadArea.classList.remove('drag-over');
                }, false);
            });

            uploadArea.addEventListener('drop', function(e) {
                const dt = e.dataTransfer;
                const files = dt.files;

                document.getElementById('excelFile').files = files;

                const event = new Event('change', { bubbles: true });
                document.getElementById('excelFile').dispatchEvent(event);
            }, false);
        }
    </script>
</body>
</html>
