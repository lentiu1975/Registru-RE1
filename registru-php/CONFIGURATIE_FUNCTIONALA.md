# CONFIGURAȚIE FUNCȚIONALĂ - NU MODIFICA!

Data: 30 Noiembrie 2025
Status: FUNCȚIONEAZĂ PERFECT

## LOCAȚIA CORECTĂ PE SERVER

**IMPORTANT:** Site-ul servește din `/vamactasud.lentiu.ro`, NU din `/public_html/vama`!

## Structura Fișierelor pe Server

```
/vamactasud.lentiu.ro/
├── index.php              (pagina principală de căutare)
├── admin.php              (pagina de administrare)
├── login.php              (autentificare)
├── logout.php             (deconectare)
├── api/
│   ├── search.php         (API căutare containere)
│   ├── test.php           (test API)
│   ├── manifests.php      (API manifeste)
│   └── import.php         (API import date)
├── config/
│   └── database.php       (configurare conexiune MySQL)
├── includes/
│   ├── functions.php      (funcții helper)
│   └── auth.php           (funcții autentificare)
└── assets/
    ├── js/
    │   └── search-app.js  (JavaScript căutare)
    └── css/
        └── search-style.css (stiluri pagină căutare)
```

## Baza de Date

**Server:** localhost
**Database:** lentiuro_vama
**User:** lentiuro_vama
**Password:** 0ZH79Fl-v9

**Tabele:**
- `manifest_entries` - 3195 containere
- `manifests` - informații manifeste
- `ships` - informații nave (nu este folosită momentan)

**Coloane disponibile în manifest_entries:**
- id
- manifest_id
- container_number
- container_type
- seal_number
- goods_description
- weight
- shipper
- consignee
- marks_numbers
- country_of_origin
- country_code
- container_image

## Script de Deployment FUNCȚIONAL

**Fișier:** `deploy_to_vamactasud.ps1`

**NU folosi alte scripturi!** Acestea uploadează în locații greșite.

## Ce Funcționează

✅ Căutare după număr container
✅ Căutare după descriere mărfuri
✅ Căutare după număr manifest
✅ Afișare imagini containere cu fallback
✅ Design responsive cu gradient mov
✅ Navigare între rezultate

## Probleme Rezolvate

1. ❌ Fișierele erau în `/public_html/vama` → ✅ Mutate în `/vamactasud.lentiu.ro`
2. ❌ JOIN cu tabela ships (lipsă date) → ✅ Eliminat JOIN-ul
3. ❌ Referințe la coloane inexistente → ✅ Folosim doar coloane disponibile
4. ❌ 404 la API → ✅ Rezolvat prin deployment corect

## URL-uri Active

- Site principal: http://vamactasud.lentiu.ro
- API test: http://vamactasud.lentiu.ro/api/test.php
- API căutare: http://vamactasud.lentiu.ro/api/search.php?q=SUDU

## Date Container

**Imagini containere:** `/Containere/{tip}/{prefix}.jpg`
- Exemplu: `/Containere/45G1/SUDU.jpg` pentru SUDU1234567
- Fallback 1: `/Containere/45G1.jpg`
- Fallback 2: `/Containere/Container.png`

**Tipuri containere suportate:** 22G1, 45G1

## ATENȚIE: NU MODIFICA

Următoarele fișiere funcționează PERFECT și NU trebuie modificate fără backup:

1. `api/search.php` - Query SQL fără JOIN ships
2. `assets/js/search-app.js` - Form submit (NU auto-search)
3. `config/database.php` - Credențiale MySQL
4. `includes/functions.php` - Funcții helper PDO
5. `deploy_to_vamactasud.ps1` - Script deployment corect

## Backup Rapid

Pentru a face deployment din nou (dacă se strică ceva):

```powershell
cd "C:\Users\Laurentiu\Desktop\Proiect RE1 - PHP"
powershell -ExecutionPolicy Bypass -File "deploy_to_vamactasud.ps1"
```

## Următoarele Modificări

Dacă vrei să faci modificări:
1. Testează LOCAL mai întâi
2. Fă backup la fișierul care funcționează
3. Upload doar fișierul modificat
4. Testează imediat pe server
5. Dacă nu merge, restaurează din backup
