# Registru import RE1

Sistem complet de gestiune pentru manifeste import cu interfață web modernă și administrare avansată.

## 📋 Descriere

**Registru import RE1** este o aplicație web full-stack pentru gestionarea manifestelor de import containerizate. Sistemul oferă:

- ✅ Căutare rapidă a containerelor după număr (minim 7 cifre)
- ✅ Gestionare multi-an cu baze de date separate
- ✅ Import/Export Excel pentru manifeste
- ✅ Auto-sincronizare tipuri containere, nave și pavilioane
- ✅ Interfață admin completă cu previzualizare imagini
- ✅ Afișare detaliată cu imagini pentru containere și nave
- ✅ Sistem autentificare securizat
- ✅ Responsive design pentru mobile și desktop

## 🏗️ Tehnologii

### Backend
- **Django 5.2.8** - Framework web Python
- **Django REST Framework** - API REST
- **PostgreSQL/SQLite** - Bază de date
- **Pillow** - Procesare imagini
- **django-import-export** - Import/Export Excel

### Frontend
- **React 19** - UI Framework
- **Axios** - HTTP Client
- **CSS3** - Styling modern

## 📦 Instalare Dezvoltare

### Cerințe
- Python 3.14+
- Node.js 16+
- npm sau yarn

### Backend Setup

1. **Clonați repository-ul**
```bash
git clone <repository-url>
cd "Proiect RE1"
```

2. **Creați mediu virtual**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalați dependențele**
```bash
pip install -r requirements.txt
```

4. **Migrare bază de date**
```bash
python manage.py migrate
```

5. **Creați superuser**
```bash
python manage.py createsuperuser
```

6. **Rulați serverul**
```bash
python manage.py runserver
```

Backend va rula pe: http://localhost:8000

### Frontend Setup

1. **Instalați dependențele**
```bash
cd frontend
npm install
```

2. **Rulați serverul de dezvoltare**
```bash
npm start
```

Frontend va rula pe: http://localhost:3000

## 🎯 Utilizare

### Acces Admin
1. Accesați: http://localhost:8000/admin
2. Login cu credențialele superuser create
3. Gestionați:
   - **Ani Baze Date** - Creați ani noi pentru baze de date separate
   - **Registru Import** - Importați/exportați manifeste Excel
   - **Tipuri Containere** - Gestionați tipuri și imagini containere
   - **Nave** - Adăugați nave cu imagini și pavilioane
   - **Pavilioane** - Gestionați pavilioane cu steaguri
   - **Utilizatori** - Administrați accesul utilizatorilor

### Import Manifeste Excel

1. Mergeți la **Admin → Registru Import 2025**
2. Click **IMPORT** (buton sus dreapta)
3. Selectați fișier Excel cu structura:
   - numar manifest
   - numar permis
   - numar pozitie
   - cerere operatiune
   - data inregistrare (format: DD.MM.YYYY)
   - container
   - numar colete
   - greutate bruta
   - descriere marfa
   - tip operatiune
   - nume nava
   - pavilion nava
   - numar sumara
   - tip container
   - linie maritima

4. Click **Submit** - sistemul va:
   - Importa manifestele
   - Auto-genera tipuri containere unice
   - Auto-crea nave și pavilioane
   - Actualiza relațiile

### Căutare Container (Interfața User)

1. Login la: http://localhost:3000
2. Selectați anul dorit
3. Introduceți număr container (minim 7 cifre)
4. Click **Căutare**
5. Navigați prin rezultate cu butoanele ◀ Anterior / Următor ▶

## 📁 Structura Proiect

```
Proiect RE1/
├── manifest_system/        # Configurare Django
│   ├── settings.py         # Setări aplicație
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI config
├── manifests/             # App principal Django
│   ├── models.py          # Modele bază de date
│   ├── views.py           # API endpoints
│   ├── serializers.py     # DRF serializers
│   ├── admin.py           # Configurare admin
│   └── management/        # Management commands
├── frontend/              # Aplicație React
│   ├── src/
│   │   ├── components/    # Componente React
│   │   ├── services/      # API client
│   │   └── App.js         # Component principal
│   └── public/            # Fișiere statice
├── media/                 # Upload-uri (imagini)
├── staticfiles/          # Fișiere statice colectate
├── requirements.txt      # Dependențe Python
├── Procfile             # Config deployment
├── runtime.txt          # Versiune Python
├── .env.example         # Template variabile mediu
├── DEPLOYMENT.md        # Ghid deployment
└── README.md            # Acest fișier
```

## 🔧 Configurare Avansată

### Auto-sincronizare Tabele

Pentru sincronizarea manuală a tabelelor de referință:

```bash
python manage.py sync_lookup_tables
```

Acest command va:
- Extrage tipuri containere unice din manifeste
- Crea/actualiza nave
- Crea/actualiza pavilioane
- Actualiza relațiile în manifeste

### Crearea unui An Nou

1. Admin → Ani Baze Date
2. Click butonul **Creare An Nou**
3. Introduceți anul (ex: 2026)
4. Click **Creare**

Acum puteți importa manifeste pentru anul nou creat.

### Gestionare Imagini

#### Containere
- Format acceptat: JPG, PNG, GIF
- Dimensiune recomandată: 800x600px
- Upload: Admin → Tipuri Containere → Edit → Imagine

#### Nave
- Format acceptat: JPG, PNG, GIF
- Dimensiune recomandată: 600x400px
- Upload: Admin → Nave → Edit → Imagine

#### Pavilioane (Steaguri)
- Format acceptat: JPG, PNG, GIF, SVG
- Dimensiune recomandată: 150x100px
- Upload: Admin → Pavilioane → Edit → Imagine

## 🚀 Deployment

Pentru deployment în producție, consultați [DEPLOYMENT.md](DEPLOYMENT.md) care include:

- Configurare pentru Heroku
- Configurare pentru Railway
- Setup VPS (DigitalOcean, Linode)
- Configurare Nginx + Gunicorn
- SSL cu Let's Encrypt
- Best practices securitate

### Quick Deploy (Heroku)

```bash
# Login Heroku
heroku login

# Creare aplicație
heroku create your-app-name

# Adaugă PostgreSQL
heroku addons:create heroku-postgresql:mini

# Deploy
git push heroku main

# Migrare
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## 🔐 Securitate

### Recomandări Producție

1. **SECRET_KEY** - Generați unul unic:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

2. **DEBUG** - Setați `DEBUG=False` în producție

3. **ALLOWED_HOSTS** - Configurați doar domeniile dvs.

4. **Database** - Folosiți PostgreSQL în producție, nu SQLite

5. **HTTPS** - Activați SSL/TLS

6. **CORS** - Configurați doar originile de încredere

## 📊 API Endpoints

### Authentication
- `POST /api/login/` - Login utilizator
- `POST /api/logout/` - Logout
- `GET /api/check-auth/` - Verificare autentificare

### Manifests
- `GET /api/manifests/` - Listă manifeste (paginate)
- `GET /api/manifests/search/?container=XXX&year=2025` - Căutare container
- `GET /api/latest-manifest/?year=2025` - Ultimul manifest actualizat

### Years
- `GET /api/years/` - Listă ani disponibili

### Reference Data
- `GET /api/container-types/` - Tipuri containere
- `GET /api/ships/` - Nave
- `GET /api/pavilions/` - Pavilioane

## 🐛 Troubleshooting

### Eroare: "No module named 'manifests'"
```bash
# Asigurați-vă că sunteți în directorul corect
cd "Proiect RE1"
python manage.py runserver
```

### Eroare: "years.map is not a function"
- Verificați că backend-ul rulează pe port 8000
- Verificați CORS settings în settings.py

### Static files nu se încarcă
```bash
python manage.py collectstatic --noinput
```

### Database locked (SQLite)
- Închideți toate conexiunile la baza de date
- Reporniți serverul Django

## 📝 Licență

Copyright © 2025. Toate drepturile rezervate.

## 👥 Contribuție

Pentru sugestii sau raportare bug-uri, deschideți un issue în repository.

## 📞 Contact

Pentru întrebări tehnice sau suport, contactați administratorul sistemului.

---

**Versiune:** 1.0
**Ultima actualizare:** 2025-11-27
