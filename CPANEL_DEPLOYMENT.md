# Deployment pe cPanel - vama.lentiu.ro

Ghid pas cu pas pentru deployment pe server cPanel.

## 🔐 Informații Server
- **Domeniu:** vama.lentiu.ro
- **cPanel URL:** https://cpanel.lentiu.ro
- **Username:** lentiuro

## 📋 Pași de Deployment

### Pasul 1: Conectare la cPanel

1. Accesați: https://cpanel.lentiu.ro
2. Login cu credențialele dvs.
3. **⚠️ IMPORTANT:** După deployment, schimbați parola pentru securitate!

### Pasul 2: Configurare Python Application

1. În cPanel, căutați **"Setup Python App"** (în secțiunea Software)
2. Click pe **"Create Application"**
3. Configurați astfel:
   - **Python Version:** 3.14 (sau cea mai apropiată versiune disponibilă: 3.11, 3.12)
   - **Application Root:** vama.lentiu.ro (sau alt director preferat)
   - **Application URL:** / (root domain)
   - **Application Startup File:** passenger_wsgi.py
   - **Application Entry Point:** application

4. Click **"Create"**

### Pasul 3: Upload Fișiere Backend

#### Opțiunea 1: File Manager (pentru fișiere mici)

1. În cPanel, deschideți **"File Manager"**
2. Navigați la directorul `vama.lentiu.ro` (sau directorul ales)
3. Upload toate fișierele proiectului EXCEPTÂND:
   - `venv/` (mediul virtual - se va recrea)
   - `node_modules/`
   - `frontend/node_modules/`
   - `db.sqlite3` (baza de date locală)
   - `.git/`
   - `__pycache__/`

#### Opțiunea 2: FTP/SFTP (recomandat pentru proiecte mari)

1. În cPanel, găsiți **"FTP Accounts"**
2. Creați un cont FTP sau folosiți contul principal
3. Folosiți un client FTP (FileZilla, WinSCP) pentru upload:
   - **Host:** ftp.lentiu.ro sau cpanel.lentiu.ro
   - **Username:** lentiuro
   - **Port:** 21 (FTP) sau 22 (SFTP)
   - **Upload la:** /home/lentiuro/vama.lentiu.ro/

#### Fișiere Importante de Upload:
```
✅ manifest_system/ (director întreg)
✅ manifests/ (director întreg)
✅ media/ (director întreg - doar structura, fără upload-uri dacă sunt mari)
✅ passenger_wsgi.py
✅ .htaccess
✅ requirements.txt
✅ manage.py
✅ db.sqlite3 (opțional - doar pentru testare, folosiți MySQL în producție)
```

### Pasul 4: Instalare Dependențe Python

1. În cPanel, accesați **"Terminal"** (sau SSH)
2. Navigați la directorul aplicației:
```bash
cd ~/vama.lentiu.ro
```

3. Activați mediul virtual creat de cPanel:
```bash
source /home/lentiuro/virtualenv/vama.lentiu.ro/3.14/bin/activate
```

4. Instalați dependențele:
```bash
pip install -r requirements.txt
```

### Pasul 5: Configurare Bază de Date

#### Opțiunea 1: MySQL (Recomandat pentru producție)

1. În cPanel, accesați **"MySQL® Databases"**
2. Creați o bază de date nouă:
   - **Database Name:** lentiuro_registru
3. Creați un utilizator:
   - **Username:** lentiuro_admin
   - **Password:** [generați o parolă puternică]
4. Adăugați utilizatorul la baza de date cu **ALL PRIVILEGES**

5. Notați:
   - **DB Name:** lentiuro_registru
   - **DB User:** lentiuro_admin
   - **DB Password:** [parola generată]
   - **DB Host:** localhost

6. Actualizați `settings.py` să folosească MySQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lentiuro_registru',
        'USER': 'lentiuro_admin',
        'PASSWORD': 'your-password-here',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

7. Instalați driver MySQL:
```bash
pip install mysqlclient
```

#### Opțiunea 2: SQLite (Doar pentru testare)

SQLite este deja configurat în settings.py pentru dezvoltare.

### Pasul 6: Migrare Bază de Date

În Terminal/SSH:

```bash
cd ~/vama.lentiu.ro
source /home/lentiuro/virtualenv/vama.lentiu.ro/3.14/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py sync_lookup_tables
```

### Pasul 7: Configurare Variabile de Mediu

Creați fișier `.env` în directorul rădăcină (prin File Manager sau Terminal):

```bash
nano ~/.env
```

Adăugați:
```env
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=vama.lentiu.ro,www.vama.lentiu.ro
CORS_ALLOWED_ORIGINS=https://vama.lentiu.ro,http://vama.lentiu.ro
CSRF_TRUSTED_ORIGINS=https://vama.lentiu.ro,http://vama.lentiu.ro
```

**Generați SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Pasul 8: Build și Deploy Frontend React

#### Pe calculatorul local:

1. Configurați API URL pentru producție:
```bash
cd frontend
```

2. Creați fișier `.env.production`:
```env
REACT_APP_API_URL=https://vama.lentiu.ro/api
```

3. Build pentru producție:
```bash
npm run build
```

4. Upload directorul `frontend/build/` pe server la:
   - `/home/lentiuro/public_html/` (pentru domeniul principal)
   - SAU `/home/lentiuro/vama.lentiu.ro/frontend/build/` (pentru organizare)

#### Configurare servire frontend:

**Opțiunea A: Subdirector separate**
- Backend API: `https://vama.lentiu.ro/api/`
- Frontend: `https://vama.lentiu.ro/` (servit din public_html)

**Opțiunea B: Toate într-un loc**
- Copiați conținutul `build/` în `vama.lentiu.ro/static_frontend/`
- Configurați Django să servească frontend-ul

### Pasul 9: Configurare SSL (HTTPS)

1. În cPanel, accesați **"SSL/TLS Status"**
2. Găsiți `vama.lentiu.ro`
3. Click **"Run AutoSSL"** pentru certificat gratuit Let's Encrypt
4. Așteptați confirmarea instalării

### Pasul 10: Configurare Domeniu

1. În cPanel, **"Domains"** → **"Subdomains"**
2. Verificați că `vama.lentiu.ro` este configurat corect
3. Document Root ar trebui să fie: `/home/lentiuro/vama.lentiu.ro/public_html` sau similar

### Pasul 11: Restart Aplicație

După fiecare modificare:

1. În **"Setup Python App"**, găsiți aplicația
2. Click pe **"Restart"** sau folosiți comanda:
```bash
touch ~/vama.lentiu.ro/tmp/restart.txt
```

### Pasul 12: Configurare Permisiuni

```bash
cd ~/vama.lentiu.ro
chmod 755 passenger_wsgi.py
chmod -R 755 media/
chmod -R 755 staticfiles/
```

## 🔧 Troubleshooting

### Eroare: "Application failed to start"

1. Verificați logs:
```bash
tail -f ~/vama.lentiu.ro/logs/error.log
```

2. Verificați că mediul virtual este activat
3. Verificați că toate dependențele sunt instalate
4. Verificați `passenger_wsgi.py`

### Eroare: 500 Internal Server Error

1. Setați `DEBUG=True` temporar pentru a vedea erorile
2. Verificați `ALLOWED_HOSTS` include domeniul
3. Verificați permisiunile fișierelor
4. Verificați configurarea bazei de date

### Static Files nu se încarcă

```bash
python manage.py collectstatic --clear --noinput
chmod -R 755 staticfiles/
```

### CORS Errors

Verificați în `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'https://vama.lentiu.ro',
    'http://vama.lentiu.ro',
]
```

## 📊 Structura Finală pe Server

```
/home/lentiuro/
├── vama.lentiu.ro/           # Aplicația Django
│   ├── manifest_system/
│   ├── manifests/
│   ├── media/
│   ├── staticfiles/
│   ├── passenger_wsgi.py
│   ├── .htaccess
│   ├── requirements.txt
│   └── manage.py
├── public_html/              # Frontend React (build)
│   ├── index.html
│   ├── static/
│   └── manifest.json
└── virtualenv/
    └── vama.lentiu.ro/
        └── 3.14/
            └── bin/
                └── python3.14
```

## 🔒 Securitate Post-Deployment

1. ✅ Schimbați parola cPanel
2. ✅ Schimbați SECRET_KEY în producție
3. ✅ Setați DEBUG=False
4. ✅ Activați SSL (HTTPS)
5. ✅ Configurați backup-uri automate
6. ✅ Limitați accesul SSH dacă este posibil
7. ✅ Folosiți parole puternice pentru baza de date

## 📞 Comenzi Utile

### Restart aplicație:
```bash
touch ~/vama.lentiu.ro/tmp/restart.txt
```

### Verificare logs:
```bash
tail -f ~/logs/error.log
tail -f ~/vama.lentiu.ro/logs/access.log
```

### Backup bază de date MySQL:
```bash
mysqldump -u lentiuro_admin -p lentiuro_registru > backup_$(date +%Y%m%d).sql
```

### Update aplicație:
```bash
cd ~/vama.lentiu.ro
source /home/lentiuro/virtualenv/vama.lentiu.ro/3.14/bin/activate
git pull  # dacă folosiți git
pip install -r requirements.txt --upgrade
python manage.py migrate
python manage.py collectstatic --noinput
touch ~/vama.lentiu.ro/tmp/restart.txt
```

## ✅ Checklist Final

- [ ] Python app creată în cPanel
- [ ] Toate fișierele uploadate
- [ ] Dependențe instalate (`pip install -r requirements.txt`)
- [ ] Bază de date configurată (MySQL recomandat)
- [ ] Migrații rulate (`python manage.py migrate`)
- [ ] Superuser creat
- [ ] Static files colectate (`collectstatic`)
- [ ] Frontend build și uploaded
- [ ] SSL activat (HTTPS)
- [ ] Variabile de mediu configurate (.env)
- [ ] DEBUG=False în producție
- [ ] ALLOWED_HOSTS configurat
- [ ] Aplicația restart-ată
- [ ] Test funcționalitate (login, căutare, admin)
- [ ] Parola cPanel schimbată

---

**Notă:** Procesul poate varia ușor în funcție de configurația specifică a cPanel-ului dvs. Dacă întâmpinați probleme, verificați documentația furnizorului de hosting sau contactați suportul tehnic.

**Versiune:** 1.0
**Data:** 2025-11-27
