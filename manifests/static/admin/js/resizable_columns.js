// Redimensionare coloane tabel admin Django cu salvare în localStorage
(function() {
    'use strict';

    // Funcție pentru a obține cheia localStorage bazată pe pagina curentă
    function getStorageKey() {
        const path = window.location.pathname;
        return 'admin_column_widths_' + path.replace(/\//g, '_');
    }

    // Funcție pentru a salva lățimile coloanelor
    function saveColumnWidths() {
        const table = document.querySelector('#result_list');
        if (!table) return;

        const headers = table.querySelectorAll('thead th');
        const widths = {};

        headers.forEach(function(th, index) {
            const columnText = th.textContent.trim();
            if (columnText && th.style.width) {
                widths[index] = {
                    name: columnText,
                    width: th.style.width
                };
            }
        });

        try {
            localStorage.setItem(getStorageKey(), JSON.stringify(widths));
        } catch (e) {
            console.error('Nu s-a putut salva lățimea coloanelor:', e);
        }
    }

    // Funcție pentru a restabili lățimile coloanelor
    function restoreColumnWidths() {
        const table = document.querySelector('#result_list');
        if (!table) return;

        try {
            const savedWidths = localStorage.getItem(getStorageKey());
            if (!savedWidths) return;

            const widths = JSON.parse(savedWidths);
            const headers = table.querySelectorAll('thead th');

            headers.forEach(function(th, index) {
                if (widths[index] && widths[index].width) {
                    th.style.width = widths[index].width;
                    th.style.minWidth = widths[index].width;
                    th.style.maxWidth = widths[index].width;
                }
            });
        } catch (e) {
            console.error('Nu s-a putut restabili lățimea coloanelor:', e);
        }
    }

    function makeColumnsResizable() {
        const table = document.querySelector('#result_list');
        if (!table) return;

        const headers = table.querySelectorAll('thead th');

        // Restabilește lățimile salvate
        restoreColumnWidths();

        headers.forEach(function(th) {
            // Adaugă tooltip cu denumirea coloanei
            const columnText = th.textContent.trim();
            if (columnText && !th.getAttribute('title')) {
                th.setAttribute('title', columnText);
            }

            // Verifică dacă resizer-ul există deja
            if (th.querySelector('.column-resizer')) return;

            // Creează un element pentru redimensionare
            const resizer = document.createElement('div');
            resizer.className = 'column-resizer';
            resizer.style.cssText = `
                position: absolute;
                top: 0;
                right: 0;
                width: 5px;
                height: 100%;
                cursor: col-resize;
                user-select: none;
                background: transparent;
            `;

            // Asigură-te că th-ul are poziție relativă
            th.style.position = 'relative';
            th.appendChild(resizer);

            let startX, startWidth;

            resizer.addEventListener('mousedown', function(e) {
                e.preventDefault();
                startX = e.pageX;
                startWidth = th.offsetWidth;

                // Schimbă cursorul pentru toată pagina
                document.body.style.cursor = 'col-resize';
                document.body.style.userSelect = 'none';

                // Adaugă un overlay transparent pentru a preveni selecția textului
                const overlay = document.createElement('div');
                overlay.id = 'resize-overlay';
                overlay.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 9999;
                    cursor: col-resize;
                `;
                document.body.appendChild(overlay);

                function doDrag(e) {
                    const width = startWidth + (e.pageX - startX);
                    if (width > 50) { // Lățime minimă
                        th.style.width = width + 'px';
                        th.style.minWidth = width + 'px';
                        th.style.maxWidth = width + 'px';
                    }
                }

                function stopDrag() {
                    document.body.style.cursor = '';
                    document.body.style.userSelect = '';
                    const overlay = document.getElementById('resize-overlay');
                    if (overlay) {
                        overlay.remove();
                    }
                    document.removeEventListener('mousemove', doDrag);
                    document.removeEventListener('mouseup', stopDrag);

                    // Salvează lățimile după redimensionare
                    saveColumnWidths();
                }

                document.addEventListener('mousemove', doDrag);
                document.addEventListener('mouseup', stopDrag);
            });

            // Evidențiază resizer-ul la hover
            resizer.addEventListener('mouseenter', function() {
                this.style.background = 'rgba(0, 120, 215, 0.3)';
            });

            resizer.addEventListener('mouseleave', function() {
                this.style.background = 'transparent';
            });
        });
    }

    // Așteaptă încărcarea completă a paginii
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', makeColumnsResizable);
    } else {
        makeColumnsResizable();
    }

    // Re-inițializează după filtrare/sortare AJAX
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                makeColumnsResizable();
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
