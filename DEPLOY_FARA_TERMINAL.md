# 🚀 Deployment FĂRĂ Terminal/SSH

Ghid complet pentru deployment pe vama.lentiu.ro **FĂRĂ acces la Terminal sau SSH**.

## 📋 Ce ai nevoie

- Acces la cPanel (https://cpanel.lentiu.ro)
- File Manager sau client FTP (FileZilla)
- Browser web
- Răbdare (procesul durează ~30-40 minute)

## 🎯 Metoda 1: Folosind Script-uri Python (CEL MAI SIMPLU)

### Pasul 1: Build Frontend (pe calculatorul tău)

Dublu-click pe:
```
BUILD_FRONTEND.bat
```

### Pasul 2: Creează Baza de Date MySQL

1. Login cPanel → **"MySQL® Databases"**
2. Create Database: `registru` → devine `lentiuro_registru`
3. Create User: `admin` → devine `lentiuro_admin` + parolă puternică
4. Add User To Database → ALL PRIVILEGES
5. **NOTEAZĂ:** Database name, username, password

### Pasul 3: Upload TOATE Fișierele Backend

Via File Manager sau FTP la `/home/lentiuro/vama_backend/`:

**Upload acestea:**
```
✅ manifest_system/ (TOT folder-ul cu subfoldere)
✅ manifests/ (TOT folder-ul cu subfoldere)
✅ media/ (doar structura, creați folder gol)
✅ staticfiles/ (creați folder gol)
✅ passenger_wsgi.py
✅ .htaccess
✅ requirements.txt
✅ manage.py
✅ .env.cpanel
✅ setup_deployment.py (NOU!)
✅ create_superuser.py (NOU!)
✅ run_setup.cgi (NOU!)
```

### Pasul 4: Configurează .env

1. File Manager → `/home/lentiuro/vama_backend/`
2. Găsește `.env.cpanel`
3. **Rename** → `.env`
4. **Edit** → Actualizează:

```env
SECRET_KEY=GENEREAZA-UNO-NOU-PE-DJECRETY.IR
DEBUG=False
ALLOWED_HOSTS=vama.lentiu.ro,www.vama.lentiu.ro

DB_ENGINE=mysql
DB_NAME=lentiuro_registru
DB_USER=lentiuro_admin
DB_PASSWORD=[PAROLA TA]
DB_HOST=localhost
DB_PORT=3306

CORS_ALLOWED_ORIGINS=https://vama.lentiu.ro,http://vama.lentiu.ro
CSRF_TRUSTED_ORIGINS=https://vama.lentiu.ro,http://vama.lentiu.ro
```

**Pentru SECRET_KEY:** Mergi pe https://djecrety.ir/ și generează unul nou

5. **Save**

### Pasul 5: Configurează create_superuser.py

1. File Manager → Găsește `create_superuser.py`
2. **Edit**
3. La începutul fișierului, schimbă:

```python
USERNAME = "admin"           # Username-ul tău
EMAIL = "admin@lentiu.ro"    # Email-ul tău
PASSWORD = "Parola123Strong!" # Parolă PUTERNICĂ!
```

4. **Save**

### Pasul 6: Setup Python Application

1. cPanel → **"Setup Python App"** (sau "Python App")
2. Click **"Create Application"**
3. Configurare:
   - **Python version:** 3.11 sau 3.12 (cel mai recent)
   - **Application root:** `vama_backend`
   - **Application URL:** `/` (sau lăsați gol)
   - **Application startup file:** `passenger_wsgi.py`
   - **Application Entry point:** `application`
4. Click **"Create"**

⏳ Așteaptă ~2-3 minute să se creeze mediul virtual

### Pasul 7: Instalează Dependențele (FĂRĂ Terminal)

#### Opțiunea A: Prin Python App Interface (dacă e disponibil)

Unele cPanel-uri au buton de instalare dependențe:
1. În **"Setup Python App"** → găsește aplicația
2. Caută buton **"Install from requirements.txt"** sau **"Run pip install"**
3. Click și așteaptă

#### Opțiunea B: Prin Cron Job (dacă Opțiunea A nu există)

1. cPanel → **"Cron Jobs"**
2. **"Add New Cron Job"**
3. Configurare:
   - **Common Settings:** Once Per Minute
   - **Command:**
   ```bash
   /home/lentiuro/virtualenv/vama_backend/3.11/bin/pip install -r /home/lentiuro/vama_backend/requirements.txt && echo "DONE" > /home/lentiuro/vama_backend/pip_install_done.txt
   ```
4. **Add New Cron Job**
5. Așteaptă 2-3 minute
6. Verifică în File Manager dacă apare fișierul `pip_install_done.txt`
7. **ȘTERGE** Cron Job-ul după ce ai verificat că e DONE

**Notă calea virtualenv:** Verifică în Python App interfața calea exactă către virtualenv. Poate fi:
- `/home/lentiuro/virtualenv/vama_backend/3.11/bin/pip`
- `/home/lentiuro/virtualenv/vama_backend/3.12/bin/pip`

### Pasul 8: Rulează Setup prin Browser

1. Setează permisiuni pentru `run_setup.cgi`:
   - File Manager → găsește `run_setup.cgi`
   - Right-click → **Permissions** → setează la `755` (rwxr-xr-x)

2. Editează `run_setup.cgi` și verifică prima linie:
   ```python
   #!/home/lentiuro/virtualenv/vama_backend/3.11/bin/python
   ```
   Actualizează calea dacă e diferită (vezi în Python App)

3. Accesează în browser:
   ```
   https://vama.lentiu.ro/run_setup.cgi
   ```

   SAU direct prin cPanel File Manager:
   - Găsește `setup_deployment.py`
   - Right-click → **Python** → **Run**

4. Ar trebui să vezi output-ul migrațiilor și setup-ului

### Pasul 9: Creează Superuser prin Browser

1. Setează permisiuni pentru `create_superuser.py` (dacă nu l-ai editat deja)
2. File Manager → găsește `create_superuser.py`
3. Right-click → **Python** → **Run**

SAU creează fișier `run_create_superuser.cgi`:

```python
#!/home/lentiuro/virtualenv/vama_backend/3.11/bin/python
import cgitb
cgitb.enable()

print("Content-Type: text/html")
print()

import sys
sys.path.insert(0, '/home/lentiuro/vama_backend')

from create_superuser import create_superuser
create_superuser()
```

Apoi accesează: `https://vama.lentiu.ro/run_create_superuser.cgi`

### Pasul 10: Upload Frontend

1. File Manager → `/home/lentiuro/public_html/`
2. **ȘTERGE** tot conținutul vechi
3. Upload TOT din `frontend/build/`:
   - index.html
   - static/ (folder întreg)
   - manifest.json
   - favicon.ico
   - robots.txt
   - asset-manifest.json

### Pasul 11: Activează SSL

1. cPanel → **"SSL/TLS Status"**
2. Găsește `vama.lentiu.ro`
3. Click **"Run AutoSSL"**
4. Așteaptă confirmarea (~1-2 minute)

### Pasul 12: Restart Aplicația

În Python App:
1. Găsește aplicația `vama_backend`
2. Click pe icon-ul **"Restart"** (circular arrow)

SAU prin File Manager:
1. Navighează la `/home/lentiuro/vama_backend/`
2. Creează folder `tmp` (dacă nu există)
3. În folder `tmp`, creează fișier gol numit `restart.txt`
4. SAU dacă `restart.txt` există, editează-l și adaugă un spațiu, apoi Save

### Pasul 13: Testează!

1. **Frontend:** https://vama.lentiu.ro
   - Ar trebui să vezi pagina de login

2. **Admin:** https://vama.lentiu.ro/admin
   - Login cu superuser creat

3. **Test complet:**
   - Login în aplicație
   - Căutare container
   - Verifică că admin funcționează

## 🔧 Metoda 2: Instalare Manuală Dependențe (dacă Metoda 1 nu merge)

### Opțiunea: Upload Pachete Pre-instalate

1. **Pe calculatorul local:**
   ```bash
   pip download -r requirements.txt -d packages/
   ```

2. **Upload folder `packages/` pe server**

3. **Creează script `install_offline.py`:**
   ```python
   import subprocess
   import os

   packages_dir = '/home/lentiuro/vama_backend/packages'
   pip_path = '/home/lentiuro/virtualenv/vama_backend/3.11/bin/pip'

   for package in os.listdir(packages_dir):
       if package.endswith('.whl') or package.endswith('.tar.gz'):
           package_path = os.path.join(packages_dir, package)
           subprocess.run([pip_path, 'install', package_path])
   ```

4. **Rulează prin File Manager** → Right-click → Python → Run

## 🐛 Troubleshooting

### Eroare: "run_setup.cgi" - 500 Internal Server Error

**Soluție:**
1. Verifică permisiuni: `755` (rwxr-xr-x)
2. Verifică prima linie din .cgi conține calea corectă către Python
3. Verifică în error_log: File Manager → `logs/error_log`

### Dependențele nu se instalează

**Soluție:**
1. Verifică că există folder `virtualenv/`
2. Verifică calea către pip în comenzi
3. Încearcă instalare manuală pachet cu pachet prin Cron Job:
   ```bash
   /home/lentiuro/virtualenv/vama_backend/3.11/bin/pip install django==5.2.8
   ```

### Application failed to start

**Soluție:**
1. Verifică `passenger_wsgi.py` există
2. Verifică `.env` există și e configurat corect
3. Verifică toate fișierele au fost uploadate
4. Setează temporar `DEBUG=True` în `.env` pentru a vedea eroarea

### Nu pot edita create_superuser.py

**Soluție:**
Creează superuser prin Django shell simulation:

1. Creează fișier `quick_superuser.py`:
```python
import os, sys, django
sys.path.insert(0, '/home/lentiuro/vama_backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'manifest_system.settings'
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Înlocuiți cu datele dvs
User.objects.create_superuser('admin', 'admin@lentiu.ro', 'Parola123!')
print("Superuser creat!")
```

2. Rulează prin File Manager → Python → Run

## ✅ Checklist Final

- [ ] Bază de date MySQL creată
- [ ] Toate fișierele backend uploadate (inclusiv script-uri)
- [ ] .env configurat corect
- [ ] Python App creată în cPanel
- [ ] Dependențe instalate (verificat prin pip_install_done.txt sau logs)
- [ ] setup_deployment.py rulat (migrații + collectstatic)
- [ ] Superuser creat (prin create_superuser.py)
- [ ] Frontend uploaded în public_html/
- [ ] SSL activat
- [ ] Aplicație restart-ată
- [ ] Test login funcționează
- [ ] Test admin funcționează

## 📝 Note Importante

1. **Calea virtualenv** poate varia. Verifică în Python App interfața.
2. **Permisiunile** pentru .cgi trebuie să fie `755`
3. **Restart aplicația** după fiecare modificare majoră
4. **Verifică logs** în `/home/lentiuro/logs/error_log`

## 🎉 Gata!

Aplicația ar trebui să fie live la:
- **Frontend:** https://vama.lentiu.ro
- **Admin:** https://vama.lentiu.ro/admin

**Username:** [din create_superuser.py]
**Password:** [din create_superuser.py]

---

**Succes cu deployment-ul fără terminal! 🚀**
