#!/usr/bin/env python
"""
Script pentru creare superuser fără terminal
Editați USERNAME, EMAIL și PASSWORD apoi rulați prin browser sau cPanel
"""
import os
import sys
import django

# ============================================
# CONFIGURAȚI AICI DATELE SUPERUSER
# ============================================
USERNAME = "admin"  # Schimbați cu username-ul dorit
EMAIL = "admin@lentiu.ro"  # Schimbați cu email-ul dvs
PASSWORD = "Parola123!"  # SCHIMBAȚI CU O PAROLĂ PUTERNICĂ!
# ============================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manifest_system.settings')

def create_superuser():
    """Creează superuser"""
    print("=" * 60)
    print("CREARE SUPERUSER")
    print("=" * 60)
    print()

    django.setup()
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        # Verifică dacă user-ul există deja
        if User.objects.filter(username=USERNAME).exists():
            print(f"⚠️  Utilizatorul '{USERNAME}' există deja!")
            user = User.objects.get(username=USERNAME)

            # Actualizează parola
            user.set_password(PASSWORD)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print(f"✓ Parola pentru '{USERNAME}' a fost actualizată!")
        else:
            # Creează superuser nou
            user = User.objects.create_superuser(
                username=USERNAME,
                email=EMAIL,
                password=PASSWORD
            )
            print(f"✓ Superuser '{USERNAME}' creat cu succes!")

        print()
        print("Detalii login:")
        print(f"  Username: {USERNAME}")
        print(f"  Password: {PASSWORD}")
        print(f"  Email: {EMAIL}")
        print()
        print("=" * 60)
        print("GATA! Puteți acum să vă logați în admin.")
        print("=" * 60)

        return True

    except Exception as e:
        print()
        print("=" * 60)
        print("EROARE!")
        print("=" * 60)
        print(f"Eroare: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = create_superuser()
    sys.exit(0 if success else 1)
