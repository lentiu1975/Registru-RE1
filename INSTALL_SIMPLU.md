# 🚀 Instalare SIMPLĂ - Pas cu Pas (fără Terminal)

## Metoda cea mai simplă pentru instalare pe cPanel

### ✅ Pasul 1: Upload Toate Fișierele

1. **File Manager** → `/home/lentiuro/vama_backend/`
2. Upload toate fișierele proiectului (inclusiv cele noi)

### ✅ Pasul 2: Instalează Dependențele

**FOLOSEȘTE ACEASTĂ COMANDĂ în Cron Job:**

```bash
source /home/lentiuro/virtualenv/vama_backend/3.11/bin/activate && cd /home/lentiuro/vama_backend && pip install PyMySQL==1.1.1 python-dotenv==1.0.1 && pip install -r requirements.txt && echo "DONE $(date)" > /home/lentiuro/vama_backend/install_log.txt
```

**Pași:**
1. cPanel → **Cron Jobs**
2. **Add New Cron Job**
3. Common Settings: **Once Per Minute**
4. Command: (copiază comanda de mai sus)
5. **Add New Cron Job**
6. Așteaptă 3-5 minute
7. File Manager → verifică dacă apare `install_log.txt` cu text "DONE"
8. **ȘTERGE** Cron Job-ul

### ✅ Pasul 3: Rulează Migrațiile

**Crează fișier nou:** `run_migrations.py` prin File Manager → New File

**Conținut:**
```python
#!/home/lentiuro/virtualenv/vama_backend/3.11/bin/python
import os
import sys

# Setează calea
sys.path.insert(0, '/home/lentiuro/vama_backend')
os.chdir('/home/lentiuro/vama_backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'manifest_system.settings'

print("=" * 60)
print("RULARE MIGRAȚII")
print("=" * 60)

import django
django.setup()

from django.core.management import call_command

try:
    # Migrații
    print("\n1. Migrații bază de date...")
    call_command('migrate', verbosity=2)
    print("✓ Migrații OK!\n")

    # Collectstatic
    print("2. Colectare static files...")
    call_command('collectstatic', '--noinput', verbosity=1)
    print("✓ Static files OK!\n")

    # Sync
    print("3. Sincronizare tabele...")
    call_command('sync_lookup_tables')
    print("✓ Sync OK!\n")

    print("=" * 60)
    print("SUCCES! Toate operațiile finalizate!")
    print("=" * 60)

except Exception as e:
    print(f"\n✗ EROARE: {e}")
    import traceback
    traceback.print_exc()
```

**Salvează fișierul**, apoi:

**Metoda A - Prin Cron Job:**
```bash
/home/lentiuro/virtualenv/vama_backend/3.11/bin/python /home/lentiuro/vama_backend/run_migrations.py > /home/lentiuro/vama_backend/migrations_output.txt 2>&1
```

Așteaptă 1-2 minute, apoi citește `migrations_output.txt` pentru a vedea rezultatul.

**Metoda B - Prin File Manager:**
1. Right-click pe `run_migrations.py`
2. Dacă vezi opțiune **"Run"** → Click
3. Dacă NU → folosește Metoda A (Cron Job)

### ✅ Pasul 4: Creează Superuser

**Editează `create_superuser.py`** (în File Manager):

Găsește la început:
```python
USERNAME = "admin"  # SCHIMBĂ AICI
EMAIL = "admin@lentiu.ro"  # SCHIMBĂ AICI
PASSWORD = "Parola123!"  # SCHIMBĂ CU PAROLĂ PUTERNICĂ!
```

Modifică cu datele tale, apoi **Save**.

**Rulează prin Cron Job:**
```bash
/home/lentiuro/virtualenv/vama_backend/3.11/bin/python /home/lentiuro/vama_backend/create_superuser.py > /home/lentiuro/vama_backend/superuser_output.txt 2>&1
```

Citește `superuser_output.txt` pentru confirmare.

### ✅ Pasul 5: Restart Aplicația

**File Manager:**
1. Navighează la `/home/lentiuro/vama_backend/`
2. Dacă NU există folder `tmp`, creează-l
3. În `tmp/`, creează fișier nou: `restart.txt` (gol)
4. SAU dacă există deja, editează-l, adaugă un spațiu, Save

**SAU în Python App:**
- Găsește aplicația
- Click pe icon **Restart** (săgeți circulare)

### ✅ Pasul 6: Testează

**Backend API:**
Accesează în browser: `https://vama.lentiu.ro/admin`

Ar trebui să vezi pagina de login Django admin.

**Login:**
- Username: (cel din create_superuser.py)
- Password: (cel din create_superuser.py)

### ✅ Pasul 7: Upload Frontend

1. File Manager → `/home/lentiuro/public_html/`
2. ȘTERGE tot conținutul vechi
3. Upload TOT din `frontend/build/`:
   - index.html
   - static/ (folder)
   - manifest.json
   - favicon.ico
   - etc.

### ✅ Pasul 8: Testează Complet

**Frontend:** https://vama.lentiu.ro
- Pagina de login React

**Admin:** https://vama.lentiu.ro/admin
- Django admin

**Test Login:** Încearcă să te loghezi în aplicație

---

## 🐛 Dacă Ceva Nu Merge

### Verifică Logs

**File Manager:**
- `/home/lentiuro/logs/error_log`
- `/home/lentiuro/vama_backend/install_log.txt`
- `/home/lentiuro/vama_backend/migrations_output.txt`
- `/home/lentiuro/vama_backend/superuser_output.txt`

### Erori Comune

**1. "No module named 'pymysql'"**
- Dependențele nu s-au instalat
- Re-rulează Cron Job din Pasul 2
- Verifică că calea virtualenv e corectă

**2. "Application failed to start"**
- Verifică `.env` există și e configurat
- Verifică `passenger_wsgi.py` există
- Setează temporar `DEBUG=True` în `.env`

**3. "Database connection error"**
- Verifică credențialele MySQL în `.env`
- Verifică că baza de date există
- Verifică că user-ul are privilegii

**4. "Static files not loading"**
- Re-rulează collectstatic
- Verifică permisiuni folder `staticfiles/`
- Restart aplicație

### Comenzi Rapide (Cron Jobs)

**Re-instalare dependențe:**
```bash
source /home/lentiuro/virtualenv/vama_backend/3.11/bin/activate && pip install -r /home/lentiuro/vama_backend/requirements.txt --force-reinstall
```

**Re-migrații:**
```bash
/home/lentiuro/virtualenv/vama_backend/3.11/bin/python /home/lentiuro/vama_backend/run_migrations.py
```

**Verificare instalare:**
```bash
/home/lentiuro/virtualenv/vama_backend/3.11/bin/pip list > /home/lentiuro/vama_backend/pip_list.txt
```

Apoi citește `pip_list.txt` să vezi ce e instalat.

---

## ✅ Checklist Rapid

- [ ] Fișiere uploadate în `/home/lentiuro/vama_backend/`
- [ ] `.env` configurat cu DB credentials și SECRET_KEY
- [ ] Python App creată în cPanel
- [ ] Dependențe instalate (verificat `install_log.txt`)
- [ ] Migrații rulate (verificat `migrations_output.txt`)
- [ ] Superuser creat (verificat `superuser_output.txt`)
- [ ] Aplicație restart-ată
- [ ] Frontend uploaded în `/home/lentiuro/public_html/`
- [ ] Test: https://vama.lentiu.ro/admin funcționează
- [ ] Test: Login în admin funcționează
- [ ] Test: Frontend se încarcă

---

**🎉 Gata! Aplicația ar trebui să fie live!**

**Probleme?** Verifică fișierele de output create de Cron Jobs pentru erori detaliate.
