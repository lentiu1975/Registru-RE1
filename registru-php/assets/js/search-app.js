document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const searchLoading = document.getElementById('searchLoading');

    let currentResults = [];
    let currentIndex = 0;

    // DOAR form submit - NU auto-search pe input
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        performSearch();
    });

    function performSearch() {
        const query = searchInput.value.trim();

        if (query.length < 2) {
            return;
        }

        searchLoading.style.display = 'block';
        searchResults.innerHTML = '';

        fetch('/api/search.php?q=' + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                searchLoading.style.display = 'none';

                if (data.error) {
                    searchResults.innerHTML = '<div style="padding: 20px; background: #ffe6e6; color: #c0392b; border-radius: 8px;">' + data.error + '</div>';
                    return;
                }

                if (!data.results || data.results.length === 0) {
                    searchResults.innerHTML = '<div style="padding: 20px; background: #e3f2fd; color: #1976d2; border-radius: 8px;">Nu s-au gasit rezultate</div>';
                    return;
                }

                currentResults = data.results;
                currentIndex = 0;
                displayCurrentResult();
            })
            .catch(error => {
                console.error('Search error:', error);
                searchLoading.style.display = 'none';
                searchResults.innerHTML = '<div style="padding: 20px; background: #ffe6e6; color: #c0392b; border-radius: 8px;">Eroare la cautare</div>';
            });
    }

    function displayCurrentResult() {
        if (currentResults.length === 0) return;

        const result = currentResults[currentIndex];
        const count = currentResults.length;

        let html = '<div class="results-navigation">';
        html += '<span class="results-count">Gasite ' + count + ' rezultate</span>';

        if (count > 1) {
            html += '<div class="navigation-buttons">';
            html += '<button onclick="window.searchApp.previousResult()" ' + (currentIndex === 0 ? 'disabled' : '') + ' class="nav-button">Anterior</button>';
            html += '<span class="current-position">' + (currentIndex + 1) + ' / ' + count + '</span>';
            html += '<button onclick="window.searchApp.nextResult()" ' + (currentIndex === count - 1 ? 'disabled' : '') + ' class="nav-button">Urmator</button>';
            html += '</div>';
        }

        html += '</div>';

        html += '<div class="results-section"><div class="result-details">';

        // Left
        html += '<div class="details-left">';
        html += '<div class="position-title">Pozitie RE1</div>';

        const manifestNumber = result.manifest_number || 'N/A';
        const containerNumber = result.container_number || 'N/A';
        const arrivalDate = result.arrival_date ? new Date(result.arrival_date).toLocaleDateString('ro-RO') : 'N/A';
        
        html += '<div class="manifest-info">' + manifestNumber + ' - ' + arrivalDate + '</div>';

        const weight = result.weight || 'N/A';
        const containerType = result.container_type || 'N/A';

        html += '<div class="info-item info-row">';
        html += '<div class="info-col"><span class="info-label">Tip container:</span><span class="info-value">' + containerType + '</span></div>';
        html += '<div class="info-col"><span class="info-label">Greutate:</span><span class="info-value">' + (weight !== 'N/A' ? weight + ' Kg' : 'N/A') + '</span></div>';
        html += '</div>';

        const marksNumbers = result.marks_numbers || 'N/A';
        html += '<div class="info-item"><span class="info-label">Tara origine:</span><span class="info-value">' + marksNumbers + '</span></div>';

        const description = result.goods_description || 'N/A';
        html += '<div class="info-item description"><span class="info-label">Descriere marfa:</span><div class="info-value">' + description + '</div></div>';

        html += '</div>';

        // Right
        html += '<div class="details-right">';
        html += '<div class="container-section">';
        html += '<div class="container-title">' + containerNumber + '</div>';

        const containerImage = result.container_image || '/Containere/Container.png';
        html += '<img src="' + containerImage + '" alt="Container" class="container-image-large" onerror="this.src=\'/Containere/Container.png\'">';

        html += '</div>';

        // Ship section removed - nu avem date in baza de date

        html += '</div>';

        html += '</div></div>';

        searchResults.innerHTML = html;
    }

    window.searchApp = {
        previousResult: function() {
            if (currentIndex > 0) {
                currentIndex--;
                displayCurrentResult();
            }
        },
        nextResult: function() {
            if (currentIndex < currentResults.length - 1) {
                currentIndex++;
                displayCurrentResult();
            }
        }
    };
});