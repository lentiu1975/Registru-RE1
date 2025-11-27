"""
WSGI config pentru cPanel Passenger
"""
import os
import sys

# Calea către directorul aplicației
INTERP = os.path.join(os.environ['HOME'], 'virtualenv', 'vama_backend', '3.11', 'bin', 'python3.11')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Adaugă calea către aplicație
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.environ['HOME'], 'vama_backend'))

# Setează modulul settings Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'manifest_system.settings'

# Încarcă variabilele de mediu din .env
from pathlib import Path
env_path = Path(__file__).resolve().parent / '.env'
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

# Importă aplicația WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
