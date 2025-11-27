# Ghid Deployment - Registru import RE1

Acest ghid vă arată cum să faceți deployment aplicației Registru import RE1 în producție.

## 📋 Cerințe

- Python 3.14.0
- Node.js 16+ și npm
- PostgreSQL (recomandat pentru producție) sau SQLite (pentru testare)
- Gunicorn (inclus în requirements.txt)
- WhiteNoise (inclus în requirements.txt)

## 🔧 Configurare Backend (Django)

### 1. Instalare dependențe

```bash
pip install -r requirements.txt
```

### 2. Configurare variabile de mediu

Creați un fișier `.env` în rădăcina proiectului (folosiți `.env.example` ca șablon):

```bash
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com
```

**IMPORTANT:** Generați un SECRET_KEY nou pentru producție:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Migrare bază de date

```bash
python manage.py migrate
```

### 4. Creați superuser

```bash
python manage.py createsuperuser
```

### 5. Colectați fișierele statice

```bash
python manage.py collectstatic --noinput
```

### 6. Sincronizați tabelele de referință

```bash
python manage.py sync_lookup_tables
```

## 🎨 Configurare Frontend (React)

### 1. Instalare dependențe

```bash
cd frontend
npm install
```

### 2. Configurare API URL

Creați fișier `.env` în directorul `frontend/`:

```bash
REACT_APP_API_URL=https://your-backend-domain.com/api
```

### 3. Build pentru producție

```bash
npm run build
```

Acest command va crea un director `build/` cu fișierele optimizate pentru producție.

## 🚀 Opțiuni de Deployment

### Opțiunea 1: Heroku

1. **Instalați Heroku CLI**

   Descărcați de la: https://devcenter.heroku.com/articles/heroku-cli

2. **Login și creare aplicație**

```bash
heroku login
heroku create your-app-name
```

3. **Adăugați PostgreSQL**

```bash
heroku addons:create heroku-postgresql:mini
```

4. **Setați variabilele de mediu**

```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
heroku config:set CORS_ALLOWED_ORIGINS="https://your-frontend-url.com"
heroku config:set CSRF_TRUSTED_ORIGINS="https://your-app-name.herokuapp.com"
```

5. **Deploy**

```bash
git push heroku main
```

6. **Rulați migrațiile**

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Opțiunea 2: Railway

1. **Creați cont pe Railway.app**

   Vizitați: https://railway.app

2. **Creați proiect nou**

   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Selectați repository-ul

3. **Configurați variabilele de mediu**

   În Railway Dashboard:
   - SECRET_KEY
   - DEBUG=False
   - ALLOWED_HOSTS
   - DATABASE_URL (Railway va genera automat pentru PostgreSQL)

4. **Deploy automat**

   Railway va detecta automat Procfile și va face deploy.

### Opțiunea 3: VPS (DigitalOcean, Linode, etc.)

1. **Instalați dependențele pe server**

```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql
```

2. **Clonați repository-ul**

```bash
git clone your-repo-url
cd your-repo
```

3. **Creați mediu virtual**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configurați PostgreSQL**

```bash
sudo -u postgres psql
CREATE DATABASE registru_import;
CREATE USER registru_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE registru_import TO registru_user;
\q
```

5. **Configurați Gunicorn**

Creați fișier service: `/etc/systemd/system/manifest.service`

```ini
[Unit]
Description=Manifest System Gunicorn
After=network.target

[Service]
User=your-user
Group=www-data
WorkingDirectory=/path/to/project
Environment="PATH=/path/to/project/venv/bin"
ExecStart=/path/to/project/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 manifest_system.wsgi:application

[Install]
WantedBy=multi-user.target
```

6. **Configurați Nginx**

Creați fișier: `/etc/nginx/sites-available/manifest`

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /path/to/project/staticfiles/;
    }

    location /media/ {
        alias /path/to/project/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

7. **Activați site-ul**

```bash
sudo ln -s /etc/nginx/sites-available/manifest /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl start manifest
sudo systemctl enable manifest
```

8. **SSL cu Let's Encrypt**

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 📦 Deployment Frontend

### Opțiunea 1: Netlify

1. **Build proiectul**

```bash
cd frontend
npm run build
```

2. **Deploy pe Netlify**

   - Mergeți pe https://netlify.com
   - Drag & drop directorul `build/`
   - Setați variabila de mediu `REACT_APP_API_URL`

### Opțiunea 2: Vercel

```bash
cd frontend
npm install -g vercel
vercel --prod
```

### Opțiunea 3: Servire din Django (nu recomandat pentru trafic mare)

Puteți servi frontend-ul direct din Django:

1. Build React:

```bash
cd frontend
npm run build
```

2. Configurați Django să servească build-ul React (necesită configurare suplimentară în urls.py)

## 🔒 Securitate

### Checklist înainte de deployment:

- [ ] SECRET_KEY unic și sigur
- [ ] DEBUG=False în producție
- [ ] ALLOWED_HOSTS configurat corect
- [ ] Database securizată (nu folosiți SQLite în producție)
- [ ] HTTPS activat (SSL certificate)
- [ ] Fișiere media securizate
- [ ] CORS configurat corect
- [ ] Strong passwords pentru admin
- [ ] Regular backups pentru baza de date

## 📊 Monitorizare și Mentenanță

### Backup bază de date

**PostgreSQL:**
```bash
pg_dump registru_import > backup_$(date +%Y%m%d).sql
```

**SQLite:**
```bash
cp db.sqlite3 backup_$(date +%Y%m%d).sqlite3
```

### Logs

```bash
# Heroku
heroku logs --tail

# VPS cu systemd
sudo journalctl -u manifest -f

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Actualizare aplicație

```bash
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart manifest  # pentru VPS
```

## 🆘 Troubleshooting

### Eroare: "DisallowedHost"
- Verificați ALLOWED_HOSTS în settings.py include domeniul dvs.

### Eroare: CSRF Failed
- Verificați CSRF_TRUSTED_ORIGINS include URL-ul frontend-ului
- Verificați că CORS_ALLOW_CREDENTIALS=True

### Static files nu se încarcă
- Rulați `python manage.py collectstatic`
- Verificați STATIC_ROOT și STATIC_URL
- Verificați configurarea WhiteNoise

### Database connection error
- Verificați DATABASE_URL
- Verificați că PostgreSQL rulează
- Verificați credentials și permissions

## 📞 Suport

Pentru probleme sau întrebări, consultați:
- Django Documentation: https://docs.djangoproject.com/
- React Documentation: https://react.dev/
- Django REST Framework: https://www.django-rest-framework.org/

---

**Versiune:** 1.0
**Ultima actualizare:** 2025-11-27
