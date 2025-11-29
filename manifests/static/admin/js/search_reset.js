// Adaugă buton Reset lângă butonul Caută în Django Admin
(function() {
    'use strict';

    function addResetButton() {
        // Găsește containerul de căutare
        const searchBar = document.querySelector('#changelist-search, #toolbar');
        if (!searchBar) return;

        // Găsește formularul de căutare
        const searchForm = searchBar.querySelector('form');
        if (!searchForm) return;

        // Verifică dacă butonul Reset există deja
        if (searchForm.querySelector('.reset-search-btn')) return;

        // Găsește butonul de Submit (Caută)
        const submitButton = searchForm.querySelector('input[type="submit"]');
        if (!submitButton) return;

        // Creează butonul Reset - stilizat IDENTIC cu butonul Caută dar verde
        const resetButton = document.createElement('input');
        resetButton.type = 'button';  // Button pentru a nu submita formularul
        resetButton.value = 'Reset';

        // Copiază TOATE clasele de la butonul Submit
        const submitClasses = submitButton.className;
        resetButton.className = submitClasses + ' reset-search-btn';

        // Copiază TOATE stilurile inline de la butonul Submit
        const computedStyle = window.getComputedStyle(submitButton);

        // Aplică stilurile copiate, dar cu culori verzi
        resetButton.style.cssText = `
            background: #d4edda !important;
            background-color: #d4edda !important;
            background-image: linear-gradient(to bottom, #d4edda, #c3e6cb) !important;
            color: #155724 !important;
            border: 1px solid #c3e6cb !important;
            border-radius: ${computedStyle.borderRadius};
            padding: ${computedStyle.padding};
            font-size: ${computedStyle.fontSize};
            font-weight: ${computedStyle.fontWeight};
            font-family: ${computedStyle.fontFamily};
            height: ${computedStyle.height};
            line-height: ${computedStyle.lineHeight};
            cursor: pointer;
            margin-left: 5px;
            vertical-align: ${computedStyle.verticalAlign};
            box-shadow: 0 1px 1px rgba(0,0,0,.1);
        `;

        // Hover effect - similar cu Django admin
        resetButton.addEventListener('mouseenter', function() {
            this.style.backgroundImage = 'linear-gradient(to bottom, #c3e6cb, #b1dfbb) !important';
            this.style.backgroundColor = '#c3e6cb !important';
        });

        resetButton.addEventListener('mouseleave', function() {
            this.style.backgroundImage = 'linear-gradient(to bottom, #d4edda, #c3e6cb) !important';
            this.style.backgroundColor = '#d4edda !important';
        });

        // Click handler - șterge căutarea și reîncarcă pagina
        resetButton.addEventListener('click', function() {
            // Golește input-ul de căutare
            const searchInput = searchForm.querySelector('input[name="q"]');
            if (searchInput) {
                searchInput.value = '';
            }

            // Construiește URL-ul fără parametrul de căutare
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.delete('q');

            // Păstrează celelalte parametri (filtre, sortare, paginare)
            // dar resetează la pagina 1
            currentUrl.searchParams.delete('p');

            // Redirecționează la URL-ul nou
            window.location.href = currentUrl.toString();
        });

        // Inserează butonul după butonul Submit
        submitButton.parentNode.insertBefore(resetButton, submitButton.nextSibling);

        console.log('Reset button added to search form');
    }

    // Așteaptă încărcarea completă a paginii
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addResetButton);
    } else {
        addResetButton();
    }

    // Observă schimbările în DOM pentru a adăuga butonul și după AJAX
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                addResetButton();
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
