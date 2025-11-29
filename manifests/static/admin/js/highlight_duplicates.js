// Evidențiază containerele duplicate cu galben și containerele cu observații cu roșu în tabelul admin
(function() {
    'use strict';

    function highlightDuplicateContainers() {
        const table = document.querySelector('#result_list');
        if (!table) return;

        // Găsește indexul coloanelor "Container" și "Observatii"
        const headers = table.querySelectorAll('thead th');
        let containerColumnIndex = -1;
        let observatiiColumnIndex = -1;

        // Verifică dacă primul header este checkbox (action-checkbox-column)
        const firstHeader = headers[0];
        const hasCheckboxColumn = firstHeader.classList.contains('action-checkbox-column');
        const headerOffset = hasCheckboxColumn ? 1 : 0;

        headers.forEach(function(th, index) {
            const headerText = th.textContent.replace(/\s+/g, ' ').trim().toLowerCase();
            // Caută exact "container" (nu "model container" sau "tip container")
            if (headerText === 'container') {
                containerColumnIndex = index - headerOffset;
            }
            if (headerText === 'observatii') {
                observatiiColumnIndex = index - headerOffset;
            }
        });

        if (containerColumnIndex === -1) {
            console.log('Container column not found. Available headers:',
                Array.from(headers).map(th => th.textContent.replace(/\s+/g, ' ').trim()));
            return;
        }

        // Colectează toate valorile din coloana Container
        const rows = table.querySelectorAll('tbody tr');
        const containerValues = [];
        const containerCells = [];

        rows.forEach(function(row) {
            const cells = row.querySelectorAll('td');
            if (cells.length > containerColumnIndex) {
                const cell = cells[containerColumnIndex];
                const value = cell.textContent.trim();

                if (value) {
                    containerValues.push(value);
                    containerCells.push(cell);
                }
            }
        });

        // Găsește valorile duplicate
        const valueCounts = {};
        containerValues.forEach(function(value) {
            valueCounts[value] = (valueCounts[value] || 0) + 1;
        });

        // Găsește care sunt duplicate
        const duplicates = Object.keys(valueCounts).filter(function(value) {
            return valueCounts[value] > 1;
        });


        // Evidențiază celulele cu valori duplicate și celulele cu observații
        let highlightedCount = 0;
        let observationsCount = 0;

        rows.forEach(function(row) {
            const cells = row.querySelectorAll('td');
            if (cells.length <= containerColumnIndex) return;

            const containerCell = cells[containerColumnIndex];
            const value = containerCell.textContent.trim();

            // Resetează stilul anterior
            containerCell.style.backgroundColor = '';
            containerCell.style.borderLeft = '';
            containerCell.classList.remove('duplicate-container');
            containerCell.classList.remove('has-observations');

            // Verifică dacă există observații cu minim 5 caractere
            let hasObservations = false;
            if (observatiiColumnIndex !== -1 && observatiiColumnIndex < cells.length) {
                const observatiiCell = cells[observatiiColumnIndex];
                const observatiiSpan = observatiiCell.querySelector('span[data-obs-length]');

                if (observatiiSpan) {
                    const obsLength = parseInt(observatiiSpan.getAttribute('data-obs-length'), 10);
                    if (obsLength >= 5) {
                        hasObservations = true;
                    }
                }
            }

            // Prioritate: roșu pentru observații, apoi galben pentru duplicate
            if (hasObservations) {
                containerCell.classList.add('has-observations');
                containerCell.style.backgroundColor = '#f8d7da';  // Roșu deschis
                containerCell.style.fontWeight = 'bold';
                containerCell.style.borderLeft = 'none';
                containerCell.setAttribute('title', 'Container cu observații');
                observationsCount++;
            } else if (valueCounts[value] > 1) {
                containerCell.classList.add('duplicate-container');
                containerCell.style.backgroundColor = '#fff3cd';  // Galben deschis
                containerCell.style.fontWeight = 'bold';
                containerCell.style.borderLeft = 'none';
                containerCell.setAttribute('title', 'Container duplicat (apare de ' + valueCounts[value] + ' ori)');
                highlightedCount++;
            }
        });

    }

    // Așteaptă încărcarea completă a paginii
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', highlightDuplicateContainers);
    } else {
        highlightDuplicateContainers();
    }

    // Re-inițializează după filtrare/sortare AJAX
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                // Așteaptă puțin pentru ca DOM-ul să se stabilizeze
                setTimeout(highlightDuplicateContainers, 100);
            }
        });
    });

    // Observă schimbările în containerul rezultatelor
    const resultsContainer = document.querySelector('#changelist');
    if (resultsContainer) {
        observer.observe(resultsContainer, {
            childList: true,
            subtree: true
        });
    }
})();
