# Registru Import RE1 - Aplicație PHP

Aplicație completă de gestionare manifeste import containere, construită cu **PHP + MySQL + Bootstrap 5**.

## 🎯 Caracteristici

✅ **Căutare rapidă** - Caută containere după număr, sigiliu, expeditor, destinatar
✅ **Import Excel automat** - Procesează fișiere .xls/.xlsx cu detectare automată coloane
✅ **Administrare completă** - Gestionare manifeste, nave, porturi
✅ **Design profesional** - Temă Navy/Ocean Blue responsivă (mobile, tablet, desktop)
✅ **Autentificare securizată** - Sistem login cu hash parole și timeout sesiune
✅ **Statistici dashboard** - Vizualizare număr manifeste, containere, nave
✅ **Istoric import-uri** - Log complet cu erori și succese
✅ **Imagini containere** - Afișare automată bazată pe prefix (GCXU, TRHU, etc.)
✅ **Drapele țări** - Imagini pentru fiecare țară de origine
✅ **REST API** - Endpoint-uri pentru toate operațiunile CRUD

## 🚀 Quick Start

### 1. Deploy Rapid

```powershell
cd "C:\Users\Laurentiu\Desktop\Proiect RE1 - PHP"
.\deploy_php.ps1
```

### 2. Configurare Bază de Date

- Accesați **cPanel → phpMyAdmin**
- Creați baza: `lentiuro_vama`
- Importați: `database.sql`
- Editați `config/database.php` cu parola

### 3. Testare

- Public: https://vama.lentiu.ro
- Admin: https://vama.lentiu.ro/admin.php
- Login: `admin` / `admin123`

**Pentru detalii complete, consultați [INSTALL.md](INSTALL.md)**

## 📁 Structură Proiect

```
/
├── index.php                 # Pagina principală - Căutare
├── admin.php                 # Panou administrare (necesită login)
├── login.php                 # Autentificare
├── logout.php                # Deconectare
├── database.sql              # Structură MySQL
├── composer.json             # Dependencies PHP
├── INSTALL.md                # Ghid instalare complet
├── deploy_php.ps1            # Script deployment fișiere
├── deploy_images.ps1         # Script deployment imagini
├── config/
│   └── database.php          # Configurare MySQL
├── api/
│   ├── manifests.php         # REST API manifeste (GET/POST/PUT/DELETE)
│   ├── search.php            # API căutare containere
│   └── import.php            # API import Excel
├── includes/
│   ├── functions.php         # Helper functions
│   └── auth.php              # Middleware autentificare
├── assets/
│   ├── css/
│   │   └── style.css         # Navy/Ocean Blue theme
│   └── js/
│       └── app.js            # JavaScript (search, import, manifests)
├── uploads/                  # Fișiere Excel importate (chmod 755)
├── images/
│   ├── containere/
│   │   ├── 20G1/            # Imagini containere 20 picioare
│   │   ├── 22G1/            # Imagini containere 22 picioare
│   │   ├── 40G1/            # Imagini containere 40 picioare
│   │   └── 45G1/            # Imagini containere 45 picioare
│   ├── drapele/             # Flag images (RO.png, DE.png, etc.)
│   └── nave/                # Ship images
└── vendor/                   # PhpSpreadsheet (după composer install)
```

## 🛠 Tehnologii

- **Backend:** PHP 7.4+ cu MySQLi (prepared statements)
- **Frontend:** Bootstrap 5.3 + JavaScript ES6 vanilla
- **Bază de date:** MySQL 8.0 cu UTF-8MB4
- **Design:** Navy/Ocean Blue professional theme
- **Excel:** PhpSpreadsheet 1.29
- **Deployment:** WinSCP FTP automation

## 🎨 Design

Temă profesională Navy/Ocean Blue:

- Gradient backgrounds: `#1e3c72` → `#2a5298`
- Ocean accents: `#4a90e2`, `#5ca9e8`
- Responsive cards cu shadow și hover effects
- Smooth transitions și animations
- Mobile-first approach

## 📊 Structură Bază de Date

**Tabele principale:**

- `manifests` - Manifeste import
- `manifest_entries` - Containere (legături către manifeste)
- `ships` - Nave
- `ports` - Porturi
- `countries` - Țări cu coduri și drapele
- `container_types` - Tipuri containere (20G1, 40G1, 45G1)
- `users` - Utilizatori (admin)
- `import_logs` - Istoric import-uri Excel

## 🔌 API Endpoints

### Manifests API
```
GET    /api/manifests.php?id={id}          # Detalii manifest
GET    /api/manifests.php?page=1&per_page=20&search=...  # Lista manifeste
POST   /api/manifests.php                  # Creare manifest
PUT    /api/manifests.php                  # Actualizare manifest
DELETE /api/manifests.php?id={id}          # Ștergere manifest
```

### Search API
```
GET /api/search.php?q=GCXU123456          # Căutare container
```

### Import API
```
POST /api/import.php                       # Import Excel (multipart/form-data)
```

## 📦 Deployment

### Deployment Complet (prima dată)

```powershell
# 1. Upload fișiere cod
.\deploy_php.ps1

# 2. Upload imagini (durează ~5-10 min)
.\deploy_images.ps1
```

### Update Rapid (doar cod)

```powershell
.\deploy_php.ps1
```

## 🔒 Securitate

- ✅ Password hashing cu `password_hash()` (bcrypt)
- ✅ Prepared statements pentru SQL (previne SQL injection)
- ✅ CSRF protection în formulare
- ✅ Session timeout (30 minute)
- ✅ Input sanitization (XSS prevention)
- ✅ File upload validation (.xls/.xlsx doar)
- ✅ Autentificare obligatorie pentru admin/API

## 📝 TODO / Îmbunătățiri Viitoare

- [ ] Export manifeste în Excel/PDF
- [ ] Rapoarte statistice avansate
- [ ] Sistem notificări email
- [ ] Multi-user cu roluri (admin, viewer)
- [ ] Dark mode toggle
- [ ] Cache pentru imagini (CDN)
- [ ] API rate limiting

## 🆚 Diferențe față de Proiectul Django

| Caracteristică | Django | PHP |
|----------------|--------|-----|
| Backend | Python 3.11 + DRF | PHP 7.4+ cu MySQLi |
| Frontend | React (SPA) | Bootstrap 5 + JS vanilla |
| Deployment | Passenger WSGI (probleme) | FTP direct (funcționează) |
| Dependencies | 23 pachete pip | 1 pachet composer |
| Complexitate | Mare | Mică |
| Performanță | Bună | Excelentă pe shared hosting |
| Ușurință hosting | Dificilă | Simplă |

## 📞 Suport

Pentru probleme:
1. Verificați log-urile PHP din cPanel
2. Consultați Browser DevTools → Console/Network
3. Citiți [INSTALL.md](INSTALL.md) pentru troubleshooting

## 📄 Licență

Copyright © 2025 Vama Lentiu. Toate drepturile rezervate.

---

**Dezvoltat cu Claude Code** | **Deployment: vama.lentiu.ro** | **Status: ✅ Production Ready**
