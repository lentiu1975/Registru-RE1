#!/home/lentiuro/virtualenv/vama_backend/3.11/bin/python
# -*- coding: utf-8 -*-
"""
Script pentru rularea migrațiilor și setup-ului fără Terminal
Rulați prin Cron Job sau File Manager
"""
import os
import sys

# Setează calea către aplicație
sys.path.insert(0, '/home/lentiuro/vama_backend')
os.chdir('/home/lentiuro/vama_backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'manifest_system.settings'

print("=" * 60)
print("SETUP APLICAȚIE - Registru import RE1")
print("=" * 60)
print()

import django
django.setup()

from django.core.management import call_command

try:
    # 1. Migrații bază de date
    print("1. Rulare migrații bază de date...")
    print("-" * 60)
    call_command('migrate', verbosity=2)
    print()
    print("✓ Migrații finalizate cu SUCCES!")
    print()

    # 2. Colectare static files
    print("2. Colectare fișiere statice...")
    print("-" * 60)
    call_command('collectstatic', '--noinput', verbosity=1)
    print()
    print("✓ Static files colectate cu SUCCES!")
    print()

    # 3. Sincronizare tabele
    print("3. Sincronizare tabele de referință...")
    print("-" * 60)
    call_command('sync_lookup_tables')
    print()
    print("✓ Tabele sincronizate cu SUCCES!")
    print()

    print("=" * 60)
    print("TOATE OPERAȚIILE FINALIZATE CU SUCCES!")
    print("=" * 60)
    print()
    print("Următorii pași:")
    print("1. Creați superuser (rulați create_superuser.py)")
    print("2. Restart aplicația în cPanel Python App")
    print("3. Accesați https://vama.lentiu.ro/admin")
    print()

except Exception as e:
    print()
    print("=" * 60)
    print("EROARE LA SETUP!")
    print("=" * 60)
    print(f"Eroare: {str(e)}")
    print()
    print("Detalii complete:")
    import traceback
    traceback.print_exc()
    print()
    print("Verificați:")
    print("- Fișierul .env există și e configurat corect")
    print("- Baza de date MySQL există")
    print("- Credențialele DB din .env sunt corecte")
    print("- Toate dependențele sunt instalate")
    sys.exit(1)

sys.exit(0)
