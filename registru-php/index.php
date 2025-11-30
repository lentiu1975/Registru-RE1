<?php
require_once 'config/database.php';
require_once 'includes/functions.php';
?>
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registru Import RE1</title>
    <link rel="stylesheet" href="/assets/css/search-style.css">
</head>
<body>
    <!-- Search Container -->
    <div class="search-container">
        <!-- Header -->
        <header class="search-header">
            <div class="header-content">
                <h1>Registru import RE1 2025</h1>
                <button onclick="window.location.href='/admin.php'" class="logout-button">Deconectare</button>
            </div>
        </header>

        <!-- Content -->
        <div class="search-content">
            <!-- Search Section -->
            <div class="search-section">
                <form id="searchForm" class="search-form">
                    <div class="form-row-horizontal">
                        <div class="form-group year-select">
                            <label for="year">An:</label>
                            <select id="year" class="year-dropdown">
                                <option value="2025" selected>2025 (Activ)</option>
                            </select>
                        </div>

                        <div class="form-group container-search">
                            <label for="container">Cautare Container (minim 7 cifre):</label>
                            <input
                                type="text"
                                id="searchInput"
                                placeholder="Ex: ABCD1234567"
                                class="container-input"
                                autocomplete="off">
                        </div>

                        <button type="submit" class="search-button">Cautare</button>
                    </div>
                </form>

                <!-- Loading Indicator -->
                <div id="searchLoading" class="loading-indicator" style="display: none;">
                    <div class="spinner"></div>
                    <p>Se cauta...</p>
                </div>

                <!-- Results Container -->
                <div id="searchResults"></div>
            </div>
        </div>
    </div>

    <script src="/assets/js/search-app.js"></script>
</body>
</html>
