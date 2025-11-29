// Mută filtrele din sidebar deasupra tabelului ca drop-down-uri
(function() {
    'use strict';

    function moveFiltersToTop() {
        const filterSidebar = document.querySelector('#changelist-filter');
        const toolbar = document.querySelector('#toolbar');

        if (!filterSidebar || !toolbar) return;

        // Verifică dacă filtrele au fost deja mutate
        if (document.querySelector('.moved-filters')) return;

        // Creează un container pentru filtrele mutate
        const filtersContainer = document.createElement('div');
        filtersContainer.className = 'moved-filters';

        // Adaugă un label pentru filtre
        const filtersLabel = document.createElement('label');
        filtersLabel.textContent = 'Filtrare:';
        filtersLabel.style.cssText = `
            font-weight: 600;
            color: #333;
            font-size: 14px;
            margin-right: 10px;
        `;
        filtersContainer.appendChild(filtersLabel);

        // Django admin folosește <details> cu <summary> pentru filtre
        const filterDetails = filterSidebar.querySelectorAll('details[data-filter-title]');

        filterDetails.forEach(function(details) {
            const filterTitle = details.getAttribute('data-filter-title');
            const filterList = details.querySelector('ul');

            if (!filterList) return;

            // Creează un select (drop-down) pentru fiecare filtru
            const select = document.createElement('select');
            select.style.cssText = `
                padding: 10px 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                line-height: 1.5;
                height: auto;
                background: white;
                cursor: pointer;
                min-width: 200px;
                transition: all 0.3s ease;
            `;

            select.addEventListener('mouseenter', function() {
                this.style.borderColor = '#667eea';
            });

            select.addEventListener('mouseleave', function() {
                this.style.borderColor = '#e0e0e0';
            });

            // Adaugă opțiunea implicită
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = filterTitle;
            select.appendChild(defaultOption);

            // Extrage toate opțiunile din lista de filtre
            const links = filterList.querySelectorAll('a');
            let hasSelected = false;

            links.forEach(function(link) {
                const option = document.createElement('option');
                // Curăță textul - elimină spațiile multiple și newline-urile
                const linkText = link.textContent.replace(/\s+/g, ' ').trim();
                option.textContent = linkText;
                option.value = link.href;

                // Verifică dacă opțiunea este selectată
                if (link.classList.contains('selected')) {
                    option.selected = true;
                    hasSelected = true;
                }

                select.appendChild(option);
            });

            // Dacă nimic nu e selectat, selectează opțiunea implicită
            if (!hasSelected) {
                defaultOption.selected = true;
            }

            // Event handler pentru schimbarea selecției
            select.addEventListener('change', function() {
                if (this.value) {
                    window.location.href = this.value;
                }
            });

            // Wrapper pentru fiecare filtru
            const filterWrapper = document.createElement('div');
            filterWrapper.style.cssText = `
                display: flex;
                flex-direction: column;
                gap: 5px;
            `;

            filterWrapper.appendChild(select);
            filtersContainer.appendChild(filterWrapper);
        });

        // Inserează containerul de filtre în toolbar
        if (filtersContainer.children.length > 1) { // Mai mult decât doar label-ul
            toolbar.appendChild(filtersContainer);
        }
    }

    // Așteaptă încărcarea completă a paginii
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', moveFiltersToTop);
    } else {
        moveFiltersToTop();
    }

    // Re-inițializează după filtrare/sortare AJAX
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                // Așteaptă puțin pentru ca DOM-ul să se stabilizeze
                setTimeout(moveFiltersToTop, 100);
            }
        });
    });

    // Observă schimbările în containerul rezultatelor
    const resultsContainer = document.querySelector('#changelist');
    if (resultsContainer) {
        observer.observe(resultsContainer, {
            childList: true,
            subtree: false
        });
    }
})();
