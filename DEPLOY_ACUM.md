# 🚀 Deployment Rapid pe vama.lentiu.ro

## ⚠️ IMPORTANT - Citește mai întâi!

**SECURITATE:** După deployment, schimbați IMEDIAT parola cPanel!

## 📦 Ce am pregătit pentru tine

Am configurat complet aplicația pentru deployment pe serverul tău cPanel. Toate fișierele sunt gata!

## 🔀 Alege Metoda de Deployment

**📌 AI DOUĂ OPȚIUNI:**

1. **CU Terminal/SSH** → Urmează pașii din acest document (mai rapid)
2. **FĂRĂ Terminal/SSH** → Vezi [DEPLOY_FARA_TERMINAL.md](DEPLOY_FARA_TERMINAL.md) (mai simplu dacă nu ai SSH)

**💡 Recomandare:** Dacă nu ai acces la Terminal în cPanel, deschide **DEPLOY_FARA_TERMINAL.md** - totul funcționează prin interfața cPanel și browser!

---

## 🎯 Pași Rapidi CU Terminal/SSH (20-30 minute)

### PASUL 1: Build Frontend React

Pe calculatorul local, dublu-click pe:
```
BUILD_FRONTEND.bat
```

Acest script va:
- Crea configurația pentru producție
- Instala dependențele npm
- Crea build-ul optimizat în `frontend/build/`

### PASUL 2: Conectare cPanel

1. Deschide browser: https://cpanel.lentiu.ro
2. Login:
   - Username: `lentiuro`
   - Password: [parola ta]

### PASUL 3: Creează Baza de Date MySQL

În cPanel:

1. Găsește **"MySQL® Databases"**
2. Secțiunea "Create New Database":
   - Database Name: `registru` (va deveni: `lentiuro_registru`)
   - Click **"Create Database"**

3. Secțiunea "MySQL Users" → "Add New User":
   - Username: `admin` (va deveni: `lentiuro_admin`)
   - Password: **[Generează o parolă puternică!]** → Notează-o!
   - Click **"Create User"**

4. Secțiunea "Add User To Database":
   - User: `lentiuro_admin`
   - Database: `lentiuro_registru`
   - Click **"Add"**
   - Bifează **"ALL PRIVILEGES"**
   - Click **"Make Changes"**

**✏️ NOTEAZĂ:**
- Database: `lentiuro_registru`
- User: `lentiuro_admin`
- Password: `[parola ta generată]`

### PASUL 4: Upload Fișiere Backend

#### Opțiunea A: File Manager (simplu)

1. În cPanel, deschide **"File Manager"**
2. Navighează la `/home/lentiuro/`
3. Creează folder nou: `vama_backend`
4. Intră în `vama_backend`
5. Click **"Upload"**
6. Upload fișierele din directorul proiectului:

**Fișiere de Upload (ZIP recomandat):**
```
✅ manifest_system/ (tot folder-ul)
✅ manifests/ (tot folder-ul)
✅ media/ (doar structura goală)
✅ passenger_wsgi.py
✅ .htaccess
✅ requirements.txt
✅ manage.py
✅ .env.cpanel (redenumește în .env după upload)
```

**NU UPLOADA:**
```
❌ venv/
❌ node_modules/
❌ frontend/node_modules/
❌ db.sqlite3
❌ .git/
❌ __pycache__/
❌ *.pyc
```

#### Opțiunea B: FTP/FileZilla (mai rapid pentru multe fișiere)

1. Deschide FileZilla
2. Conectare:
   - Host: `ftp.lentiu.ro`
   - Username: `lentiuro`
   - Password: [parola cPanel]
   - Port: 21

3. Navigare Remote: `/home/lentiuro/vama_backend/`
4. Drag & Drop fișierele enumerate mai sus

### PASUL 5: Configurează Fișierul .env

În cPanel File Manager:

1. Navighează la `/home/lentiuro/vama_backend/`
2. Găsește fișierul `.env.cpanel`
3. **Right-click → Rename → `.env`**
4. **Right-click → Edit**
5. Actualizează:

```env
SECRET_KEY=[GENEREAZA UNO NOU - vezi mai jos]
DEBUG=False
ALLOWED_HOSTS=vama.lentiu.ro,www.vama.lentiu.ro

DB_ENGINE=mysql
DB_NAME=lentiuro_registru
DB_USER=lentiuro_admin
DB_PASSWORD=[PAROLA TA DE LA PASUL 3]
DB_HOST=localhost
DB_PORT=3306

CORS_ALLOWED_ORIGINS=https://vama.lentiu.ro,http://vama.lentiu.ro
CSRF_TRUSTED_ORIGINS=https://vama.lentiu.ro,http://vama.lentiu.ro
```

**Generează SECRET_KEY:** Folosește Terminal (pasul următor) sau online:
https://djecrety.ir/

6. **Save Changes**

### PASUL 6: Setup Python Application

1. În cPanel, găsește **"Setup Python App"**
2. Click **"Create Application"**
3. Configurare:
   - Python version: **3.11** sau **3.12** (cel mai recent disponibil)
   - Application root: `vama_backend`
   - Application URL: deixă gol sau `/`
   - Application startup file: `passenger_wsgi.py`
   - Application Entry point: `application`

4. Click **"Create"**

### PASUL 7: Terminal - Instalare Dependențe

1. În cPanel, găsește **"Terminal"** (sau SSH)
2. Rulați comenzile:

```bash
# Navigare la aplicație
cd ~/vama_backend

# Găsește calea către virtualenv din interfața Python App
# De obicei va fi ceva gen:
source /home/lentiuro/virtualenv/vama_backend/3.11/bin/activate

# Instalare dependențe
pip install -r requirements.txt

# Generare SECRET_KEY (copiază output-ul în .env)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Migrare bază de date
python manage.py migrate

# Creare superuser
python manage.py createsuperuser
# Introduceți: username, email (opțional), password

# Colectare static files
python manage.py collectstatic --noinput

# Sincronizare tabele
python manage.py sync_lookup_tables

# Restart aplicație
mkdir -p tmp
touch tmp/restart.txt
```

### PASUL 8: Upload Frontend React

1. În cPanel File Manager, navighează la `/home/lentiuro/public_html/`
2. **ȘTERGE** toate fișierele vechi (dacă există)
3. Upload tot conținutul din `frontend/build/`:
   - `index.html`
   - `static/` (folder întreg)
   - `manifest.json`
   - `favicon.ico`
   - etc.

**Structura finală în public_html:**
```
public_html/
├── index.html
├── static/
│   ├── css/
│   ├── js/
│   └── media/
├── manifest.json
└── favicon.ico
```

### PASUL 9: Configurare SSL (HTTPS)

1. În cPanel, găsește **"SSL/TLS Status"**
2. Găsește `vama.lentiu.ro`
3. Click **"Run AutoSSL"**
4. Așteaptă confirmarea (1-2 minute)

### PASUL 10: Configurare Domeniu

1. În cPanel, **"Domains"** sau **"Subdomains"**
2. Verifică că `vama.lentiu.ro` punctează la:
   - Document Root: `/home/lentiuro/public_html`

3. Pentru API, adaugă în `.htaccess` din `public_html`:

Creează `/home/lentiuro/public_html/.htaccess`:
```apache
# Redirecționare API către backend
RewriteEngine On
RewriteCond %{REQUEST_URI} ^/api/
RewriteRule ^api/(.*)$ http://127.0.0.1:8000/api/$1 [P,L]
RewriteCond %{REQUEST_URI} ^/admin/
RewriteRule ^admin/(.*)$ http://127.0.0.1:8000/admin/$1 [P,L]
RewriteCond %{REQUEST_URI} ^/media/
RewriteRule ^media/(.*)$ /home/lentiuro/vama_backend/media/$1 [L]
```

SAU mai simplu, configurează subdomeniile:
- Frontend: `vama.lentiu.ro` → `/public_html`
- Backend API: `api.vama.lentiu.ro` → `/vama_backend`

### PASUL 11: Test Aplicația

1. **Frontend:** https://vama.lentiu.ro
   - Ar trebui să vezi pagina de login

2. **Admin:** https://vama.lentiu.ro/admin sau https://vama.lentiu.ro:8000/admin
   - Login cu superuser creat

3. **Test login & căutare container**

## 🔧 Troubleshooting Rapid

### Eroare: "Application failed to start"

```bash
cd ~/vama_backend
tail -f logs/error.log
```

Verifică:
- Toate dependențele instalate: `pip list`
- Fișierul `.env` există și e configurat corect
- `passenger_wsgi.py` există

### Eroare: 500 Internal Server Error

Setează temporar în `.env`:
```env
DEBUG=True
```
Apoi restart:
```bash
touch ~/vama_backend/tmp/restart.txt
```

Vezi eroarea în browser, apoi **setează înapoi DEBUG=False**!

### Frontend nu se încarcă

Verifică:
- Fișierele sunt în `/public_html/`
- `index.html` există
- Permisiuni: `chmod 755 -R /home/lentiuro/public_html/`

### API nu răspunde

1. Verifică Python App în cPanel că rulează
2. Verifică portul aplicației (de obicei 8000)
3. Testează direct: `curl http://127.0.0.1:8000/api/years/`

### CORS Errors

În `.env`, verifică:
```env
CORS_ALLOWED_ORIGINS=https://vama.lentiu.ro,http://vama.lentiu.ro
CSRF_TRUSTED_ORIGINS=https://vama.lentiu.ro,http://vama.lentiu.ro
```

## 📊 Comenzi Utile

### Restart aplicație:
```bash
touch ~/vama_backend/tmp/restart.txt
```

### Vezi logs:
```bash
tail -f ~/vama_backend/logs/error.log
```

### Update aplicație:
```bash
cd ~/vama_backend
source /home/lentiuro/virtualenv/vama_backend/3.11/bin/activate
pip install -r requirements.txt --upgrade
python manage.py migrate
python manage.py collectstatic --noinput
touch tmp/restart.txt
```

### Backup bază de date:
```bash
mysqldump -u lentiuro_admin -p lentiuro_registru > backup_$(date +%Y%m%d).sql
```

## ✅ Checklist Final

- [ ] Baza de date MySQL creată
- [ ] User MySQL creat cu privilegii
- [ ] Fișiere backend uploadate
- [ ] Fișier `.env` configurat (SECRET_KEY, DB credentials)
- [ ] Python App creată în cPanel
- [ ] Dependențe instalate (`pip install -r requirements.txt`)
- [ ] Migrații rulate (`python manage.py migrate`)
- [ ] Superuser creat
- [ ] Static files colectate
- [ ] Frontend build și uploaded în `public_html/`
- [ ] SSL activat (HTTPS)
- [ ] Test: Login funcționează
- [ ] Test: Admin funcționează
- [ ] Test: Căutare container funcționează
- [ ] Parola cPanel schimbată!

## 🎉 Finalizare

Aplicația ar trebui să fie live la:
- **Frontend:** https://vama.lentiu.ro
- **Admin:** https://vama.lentiu.ro/admin

**Username:** [cel creat cu createsuperuser]
**Password:** [parola setată]

## 📞 Suport

Pentru probleme, verifică:
1. Logs: `~/vama_backend/logs/error.log`
2. Python App Status în cPanel
3. Browser Console pentru erori JavaScript
4. Network tab pentru erori API

---

**Succes cu deployment-ul! 🚀**

**Nu uita:** Schimbă parola cPanel după finalizare!
