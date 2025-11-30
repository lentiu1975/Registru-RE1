# Ghid Instalare Registru Import RE1 - PHP

## Pași Instalare

### 1. Crearea Bazei de Date MySQL

Conectați-vă la phpMyAdmin din cPanel:

1. Accesați cPanel → MySQL Databases sau Database Wizard
2. Creați o bază de date nouă: `lentiuro_vama`
3. Creați un utilizator: `lentiuro_vama`
4. Setați o parolă (salvați-o!)
5. Adăugați utilizatorul la bază de date cu ALL PRIVILEGES
6. Importați fișierul `database.sql` în baza de date

**Alternativ - SQL Direct:**

```sql
CREATE DATABASE lentiuro_vama CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Apoi rulați conținutul din `database.sql`

### 2. Configurare Conexiune Bază de Date

Editați `config/database.php` și completați credențialele de producție:

```php
define('DB_HOST_PROD', 'localhost');
define('DB_USER_PROD', 'lentiuro_vama');  // Userul din cPanel
define('DB_PASS_PROD', 'PAROLA_TA_AICI');  // Parola setată
define('DB_NAME_PROD', 'lentiuro_vama');   // Numele bazei de date
```

### 3. Instalare PhpSpreadsheet (pentru Import Excel)

**Opțiunea 1 - Prin Composer (recomandat):**

Dacă aveți SSH acces:

```bash
cd /home/lentiuro/public_html/vama
composer install
```

**Opțiunea 2 - Manual (dacă nu aveți Composer):**

1. Descărcați PhpSpreadsheet: https://github.com/PHPOffice/PhpSpreadsheet/releases
2. Extrageți în directorul `vendor/`
3. Sau folosiți PHP Archive (.phar) dacă este disponibil pe server

**Opțiunea 3 - Fără PhpSpreadsheet (import simplificat):**

Puteți folosi funcția `fgetcsv()` pentru fișiere CSV în loc de Excel.

### 4. Upload Fișiere pe Server

Folosind FTP/WinSCP, încărcați toate fișierele în:

```
/home/lentiuro/public_html/vama/
```

**Structură Directoare:**

```
vama/
├── index.php
├── admin.php
├── login.php
├── logout.php
├── composer.json
├── database.sql
├── config/
├── api/
├── includes/
├── assets/
├── uploads/         (permisiuni: 755)
├── images/
│   ├── containere/
│   ├── drapele/
│   └── nave/
└── vendor/          (după composer install)
```

### 5. Setare Permisiuni

```bash
chmod 755 /home/lentiuro/public_html/vama
chmod 755 /home/lentiuro/public_html/vama/uploads
chmod 644 /home/lentiuro/public_html/vama/*.php
```

### 6. Testare

1. Accesați: https://vama.lentiu.ro
2. Ar trebui să vedeți pagina de căutare
3. Accesați: https://vama.lentiu.ro/admin.php
4. Autentificare:
   - Username: `admin`
   - Parolă: `admin123`

**IMPORTANT:** Schimbați parola după prima autentificare!

### 7. Schimbare Parolă Admin

Conectați-vă la phpMyAdmin și rulați:

```sql
UPDATE users
SET password = '$2y$10$HASH_AICI'
WHERE username = 'admin';
```

Pentru a genera hash:

```php
<?php
echo password_hash('PAROLA_NOUA', PASSWORD_DEFAULT);
?>
```

## Troubleshooting

### Eroare: "Class 'PhpOffice\PhpSpreadsheet\IOFactory' not found"

PhpSpreadsheet nu este instalat. Urmați pașii de la secțiunea 3.

### Eroare: "Connection failed"

Verificați credențialele din `config/database.php`

### 404 Not Found

Verificați că fișierele sunt în directorul corect: `/home/lentiuro/public_html/vama/`

### Upload Excel nu funcționează

1. Verificați că directorul `uploads/` există și are permisiuni 755
2. Verificați că PhpSpreadsheet este instalat
3. Verificați log-urile PHP pentru erori

### Imagini nu se afișează

1. Copiați folderele `Containere/`, `Drapele/`, `Nave/` din proiectul Django
2. Plasați-le în `images/containere/`, `images/drapele/`, `images/nave/`

## Caracteristici

✅ Căutare rapidă containere
✅ Import Excel automat
✅ Administrare manifeste
✅ Design responsiv Navy/Ocean blue
✅ Autentificare sigură
✅ Istoric import-uri
✅ Imagini containere, drapele, nave
✅ Statistici dashboard

## Suport

Pentru probleme sau întrebări, verificați:
- Fișierele de log PHP din cPanel
- Console browser pentru erori JavaScript
- Network tab pentru erori API

## Licență

Copyright © 2025 Vama Lentiu. Toate drepturile rezervate.
