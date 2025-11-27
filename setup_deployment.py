#!/usr/bin/env python
"""
Script de setup pentru deployment fără acces la terminal
Rulați acest script prin cPanel Python App sau prin browser
"""
import os
import sys
import django

# Setează calea către proiect
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Setează settings Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manifest_system.settings')

def run_setup():
    """Rulează toate comenzile de setup"""
    print("=" * 60)
    print("SETUP DEPLOYMENT - Registru import RE1")
    print("=" * 60)
    print()

    # Inițializează Django
    django.setup()

    from django.core.management import call_command
    from django.contrib.auth import get_user_model

    try:
        # 1. Migrare bază de date
        print("1. Rulare migrații bază de date...")
        call_command('migrate', verbosity=2)
        print("✓ Migrații finalizate!\n")

        # 2. Colectare static files
        print("2. Colectare fișiere statice...")
        call_command('collectstatic', '--noinput', verbosity=2)
        print("✓ Fișiere statice colectate!\n")

        # 3. Sincronizare tabele
        print("3. Sincronizare tabele de referință...")
        call_command('sync_lookup_tables')
        print("✓ Tabele sincronizate!\n")

        # 4. Verificare superuser
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            print("4. ATENȚIE: Nu există superuser!")
            print("   Trebuie creat manual prin Django admin sau...")
            print("   Rulați create_superuser.py separat")
        else:
            print("4. ✓ Superuser există deja")

        print()
        print("=" * 60)
        print("SETUP FINALIZAT CU SUCCES!")
        print("=" * 60)
        print()
        print("Următorii pași:")
        print("1. Restart aplicația în cPanel Python App")
        print("2. Accesați https://vama.lentiu.ro")
        print("3. Dacă nu aveți superuser, rulați create_superuser.py")

        return True

    except Exception as e:
        print()
        print("=" * 60)
        print("EROARE LA SETUP!")
        print("=" * 60)
        print(f"Eroare: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_setup()
    sys.exit(0 if success else 1)
