# 🔧 FIX pentru Eroarea 404 la /admin

## 🎯 Problema Identificată

Din logs:
```
cannot determine application type at /home/lentiuro/vama_backend/, disable it.
File not found [/home/lentiuro/vama.lentiu.ro/admin]
```

**Cauza:** Passenger nu poate găsi și porni aplicația Django, astfel că serverul caută un fișier fizic `/admin` în loc să trimită request-ul către Django.

## ✅ Soluția - Pași de Urmat

### 1. Verifică și Actualizează Fișierele

Am actualizat două fișiere critice:

#### A. `.htaccess`
```apache
PassengerAppRoot /home/lentiuro/vama_backend
PassengerPython /home/lentiuro/virtualenv/vama_backend/3.11/bin/python3.11
```

#### B. `passenger_wsgi.py`
- Am adăugat configurarea corectă a Python interpreter
- Am adăugat încărcarea automată a fișierului `.env`

### 2. Upload Fișierele Actualizate pe Server

**Prin File Manager:**
1. Conectează-te la cPanel → File Manager
2. Navighează la `/home/lentiuro/vama_backend/`
3. Upload fișierele actualizate:
   - `.htaccess` (suprascrie cel existent)
   - `passenger_wsgi.py` (suprascrie cel existent)

**SAU prin FTP:**
1. Conectează-te cu FileZilla la `ftp.lentiu.ro`
2. Upload la `/home/lentiuro/vama_backend/`

### 3. Verifică Configurarea Python App în cPanel

1. Deschide cPanel → **"Setup Python App"**
2. Găsește aplicația (probabil `vama_backend`)
3. Verifică setările:
   - **Application root:** `vama_backend` (NU `vama.lentiu.ro`)
   - **Python version:** Cea instalată (3.11, 3.12, sau 3.13)
   - **Application startup file:** `passenger_wsgi.py`
   - **Application entry point:** `application`

4. **IMPORTANT:** Notează versiunea Python și calea exactă a virtualenv din interfață:
   ```
   De exemplu: /home/lentiuro/virtualenv/vama_backend/3.11/bin/python3.11
   ```

5. Dacă versiunea diferă de 3.11, actualizează în ambele fișiere:
   - `.htaccess` linia 6
   - `passenger_wsgi.py` linia 8

### 4. Verifică Fișierul .env

1. În File Manager, navighează la `/home/lentiuro/vama_backend/`
2. Verifică că există fișierul `.env` (NU `.env.cpanel`)
3. Editează `.env` și asigură-te că are:

```env
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=vama.lentiu.ro,www.vama.lentiu.ro

DB_ENGINE=mysql
DB_NAME=lentiuro_registru
DB_USER=lentiuro_admin
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=3306

CORS_ALLOWED_ORIGINS=https://vama.lentiu.ro,http://vama.lentiu.ro
CSRF_TRUSTED_ORIGINS=https://vama.lentiu.ro,http://vama.lentiu.ro
```

### 5. Verifică Dependențele Python

Conectează-te prin Terminal (cPanel → Terminal) și rulează:

```bash
cd ~/vama_backend

# Activează virtualenv - ajustează versiunea conform Setup Python App
source ~/virtualenv/vama_backend/3.11/bin/activate

# Verifică Django instalat
python -c "import django; print(django.VERSION)"

# Dacă lipsește, reinstalează
pip install -r requirements.txt

# Verifică că toate sunt instalate
pip list | grep -E "Django|mysqlclient|djangorestframework|python-dotenv"
```

### 6. Verifică Permisiunile Fișierelor

```bash
cd ~/vama_backend

# Setează permisiuni corecte
chmod 755 passenger_wsgi.py
chmod 644 .htaccess
chmod 640 .env
chmod 755 manifest_system/
chmod 755 manifests/
```

### 7. Rulează Migrațiile (Dacă Nu Ai Făcut Deja)

```bash
cd ~/vama_backend
source ~/virtualenv/vama_backend/3.11/bin/activate

# Rulează migrații
python manage.py migrate

# Colectează static files pentru admin
python manage.py collectstatic --noinput

# Creează superuser dacă nu există
python manage.py createsuperuser
```

### 8. Restart Aplicația

**Metoda 1: Prin Terminal**
```bash
mkdir -p ~/vama_backend/tmp
touch ~/vama_backend/tmp/restart.txt
```

**Metoda 2: Prin cPanel**
1. Setup Python App → Găsește aplicația
2. Click pe butonul **"Restart"**

### 9. Verifică Logs pentru Erori

```bash
# Vezi ultimele erori
tail -n 50 ~/vama_backend/logs/error.log

# SAU logs Passenger
tail -n 50 ~/logs/vama_backend_error.log
```

### 10. Testează Aplicația

După restart, verifică:

1. **Admin:** https://vama.lentiu.ro/admin
   - Ar trebui să vezi pagina de login Django admin
   - Login cu superuser-ul creat

2. **API:** https://vama.lentiu.ro/api/
   - Ar trebui să primești un răspuns JSON sau pagină REST Framework

## 🔍 Dacă Tot Nu Merge

### Verificare Suplimentară 1: Python Path

Creează un fișier test `test_wsgi.py` în `/home/lentiuro/vama_backend/`:

```python
import sys
print("Python version:", sys.version)
print("Python path:", sys.executable)
print("Sys.path:", sys.path)

try:
    import django
    print("Django found:", django.__version__)
except ImportError as e:
    print("Django NOT found:", e)
```

Apoi în Terminal:
```bash
cd ~/vama_backend
source ~/virtualenv/vama_backend/3.11/bin/activate
python test_wsgi.py
```

### Verificare Suplimentară 2: Test Manual Django

```bash
cd ~/vama_backend
source ~/virtualenv/vama_backend/3.11/bin/activate
python manage.py check
python manage.py runserver 0.0.0.0:8080
```

Dacă pornește, înseamnă că Django merge, dar Passenger nu îl găsește.

### Verificare Suplimentară 3: DEBUG Mode Temporar

În `.env`, setează:
```env
DEBUG=True
```

Restart aplicația și accesează https://vama.lentiu.ro/admin în browser. Vei vedea eroarea detaliată Django.

**NU UITA:** Setează înapoi `DEBUG=False` după debugging!

## 📞 Probleme Comune și Soluții

### Eroare: "Module 'django' not found"
```bash
cd ~/vama_backend
source ~/virtualenv/vama_backend/3.11/bin/activate
pip install django
```

### Eroare: "No module named 'mysqlclient'"
```bash
pip install mysqlclient
# SAU
pip install pymysql
```

### Eroare: "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Eroare: "ALLOWED_HOSTS"
În `.env`:
```env
ALLOWED_HOSTS=vama.lentiu.ro,www.vama.lentiu.ro,127.0.0.1,localhost
```

### Passenger Tot Nu Pornește

Verifică că Python App în cPanel are:
- Status: **Running** (verde)
- Dacă e **Stopped** (roșu), click **Start**

## 🎯 Checklist Final

- [ ] `.htaccess` actualizat și uploaded
- [ ] `passenger_wsgi.py` actualizat și uploaded
- [ ] Python App configurată corect în cPanel (path: `vama_backend`)
- [ ] Versiunea Python din `.htaccess` și `passenger_wsgi.py` match cu cea din Setup Python App
- [ ] Fișier `.env` există și e configurat corect
- [ ] Toate dependențele instalate (`pip install -r requirements.txt`)
- [ ] Migrații rulate (`python manage.py migrate`)
- [ ] Static files colectate (`python manage.py collectstatic`)
- [ ] Superuser creat (`python manage.py createsuperuser`)
- [ ] Permisiuni corecte pe fișiere
- [ ] Aplicația restart-ată (`touch tmp/restart.txt`)
- [ ] Test: https://vama.lentiu.ro/admin funcționează

## 🎉 Succes!

După acești pași, `/admin` ar trebui să funcționeze. Dacă întâmpini probleme, verifică logs-urile și contactează-mă cu outputul exact al erorii.

---

**Data:** 2025-11-27
**Status:** Fix pentru 404 Error pe /admin
