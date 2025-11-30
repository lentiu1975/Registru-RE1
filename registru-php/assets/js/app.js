/**
 * Search functionality with React-style layout
 */

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const searchLoading = document.getElementById('searchLoading');

    let searchTimeout = null;
    let currentResults = [];
    let currentIndex = 0;

    if (!searchInput || !searchResults) {
        console.error('Search elements not found');
        return;
    }

    function performSearch(query) {
        if (!query || query.trim().length < 2) {
            searchResults.innerHTML = '<div class="text-center py-5"><i class="bi bi-search" style="font-size: 4rem; color: #ddd;"></i><p class="text-muted mt-3">IntroduceÈ›i un termen de cÄƒutare pentru a vedea rezultatele</p></div>';
            if (searchLoading) searchLoading.style.display = 'none';
            return;
        }

        if (searchLoading) searchLoading.style.display = 'block';
        searchResults.innerHTML = '';

        fetch('/api/search.php?q=' + encodeURIComponent(query))
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (searchLoading) searchLoading.style.display = 'none';

                if (data.error) {
                    searchResults.innerHTML = '<div class="alert alert-danger"><i class="bi bi-exclamation-triangle"></i> ' + data.error + '</div>';
                    return;
                }

                if (!data.results || data.results.length === 0) {
                    searchResults.innerHTML = '<div class="alert alert-info"><i class="bi bi-info-circle"></i> Nu s-au gasit rezultate pentru "' + data.query + '"</div>';
                    return;
                }

                displayResults(data.results, data.count);
            })
            .catch(error => {
                console.error('Search error:', error);
                if (searchLoading) searchLoading.style.display = 'none';
                searchResults.innerHTML = '<div class="alert alert-danger"><i class="bi bi-exclamation-triangle"></i> Eroare la cautare. Va rugam incercati din nou.</div>';
            });
    }

    function displayResults(results, count) {
        currentResults = results;
        currentIndex = 0;
        displayCurrentResult();
    }

    function displayCurrentResult() {
        if (currentResults.length === 0) return;

        const result = currentResults[currentIndex];
        const count = currentResults.length;

        let html = '<div class="results-navigation mb-4">';
        html += '<div class="d-flex justify-content-between align-items-center flex-wrap gap-3">';
        html += '<span class="results-count fw-bold" style="color: #667eea; font-size: 1.1rem;">Gasite ' + count + ' rezultate</span>';

        if (count > 1) {
            html += '<div class="navigation-buttons">';
            html += '<button onclick="window.searchApp.previousResult()" ' + (currentIndex === 0 ? 'disabled' : '') + ' class="btn btn-sm btn-primary me-2">â—€ Anterior</button>';
            html += '<span class="current-position mx-2 fw-semibold">' + (currentIndex + 1) + ' / ' + count + '</span>';
            html += '<button onclick="window.searchApp.nextResult()" ' + (currentIndex === count - 1 ? 'disabled' : '') + ' class="btn btn-sm btn-primary">Urmator â–¶</button>';
            html += '</div>';
        }

        html += '</div></div>';

        html += '<div class="results-section">';
        html += '<div class="result-details">';

        html += '<div class="details-left">';
        html += '<div class="position-title">Pozitie RE1</div>';

        const manifestNumber = result.manifest_number || 'N/A';
        const containerNumber = result.container_number || 'N/A';
        const arrivalDate = result.arrival_date ? new Date(result.arrival_date).toLocaleDateString('ro-RO') : 'N/A';

        html += '<div class="manifest-info">' + manifestNumber + ' â€“ ' + arrivalDate + '</div>';

        const weight = result.weight || 'N/A';
        const sealNumber = result.seal_number || 'N/A';

        html += '<div class="info-item info-row">';
        html += '<div class="info-col"><span class="info-label">Sigiliu:</span><span class="info-value">' + sealNumber + '</span></div>';
        html += '<div class="info-col"><span class="info-label">Greutate:</span><span class="info-value">' + (weight !== 'N/A' ? weight + ' Kg' : 'N/A') + '</span></div>';
        html += '</div>';

        const containerType = result.container_type || 'N/A';
        html += '<div class="info-item"><span class="info-label">Tip container:</span><span class="info-value">' + containerType + '</span></div>';

        const description = result.goods_description || 'N/A';
        html += '<div class="info-item description"><span class="info-label">Descriere marfa:</span><div class="info-value">' + description + '</div></div>';

        html += '</div>';

        html += '<div class="details-right">';
        html += '<div class="container-section">';
        html += '<div class="container-title">' + containerNumber + '</div>';

        const containerImage = result.container_image || '/assets/images/container_default.png';
        html += '<img src="' + containerImage + '" alt="Container" class="container-image-large" onerror="this.src=\'/assets/images/container_default.png\'">';

        html += '</div></div>';

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

    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();

        if (query.length < 2) {
            searchResults.innerHTML = '<div class="text-center py-5"><i class="bi bi-search" style="font-size: 4rem; color: #ddd;"></i><p class="text-muted mt-3">Introduceti un termen de cautare pentru a vedea rezultatele</p></div>';
            if (searchLoading) searchLoading.style.display = 'none';
            return;
        }

        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 500);
    });

    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            clearTimeout(searchTimeout);
            performSearch(this.value.trim());
        }
    });
});
