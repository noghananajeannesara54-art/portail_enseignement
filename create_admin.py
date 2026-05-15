#!/usr/bin/env python
"""
Script pour créer un compte administrateur
"""

import os
import sys

# Configuration de Django pour MySQL
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portail_enseignement.settings')

try:
    import django
    from django.conf import settings
    
    # Configuration minimale
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'portail_enseignement',
                'USER': 'root',
                'PASSWORD': '',
                'HOST': '127.0.0.1',
                'PORT': '3306',
                'OPTIONS': {
                    'charset': 'utf8mb4',
                },
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'core',
        ],
        SECRET_KEY='temp-key',
        USE_TZ=False,
    )
    
    django.setup()
    
    from django.contrib.auth.models import User
    
    print("=== CRÉATION COMPTE ADMINISTRATEUR ===")
    
    # Vérifier si l'admin existe déjà
    admin_username = "admin"
    
    if User.objects.filter(username=admin_username).exists():
        print(f"❌ L'utilisateur '{admin_username}' existe déjà!")
        
        # Afficher les utilisateurs existants
        users = User.objects.all()
        print(f"\n📊 Utilisateurs existants ({users.count()}):")
        for user in users:
            is_staff = "👨‍💼 Admin" if user.is_staff else "👤 User"
            is_superuser = "🔧 Super" if user.is_superuser else ""
            print(f"   {is_staff} {user.username} {is_superuser}")
        
        print(f"\n💡 Utilisez un nom d'utilisateur existant ou supprimez l'admin existant")
    else:
        # Créer le superutilisateur
        admin_user = User.objects.create_superuser(
            username=admin_username,
            email='admin@enseignement-sup.ga',
            password='admin123'
        )
        
        print(f"✅ Administrateur créé avec succès!")
        print(f"\n👤 Identifiants de connexion:")
        print(f"   Nom d'utilisateur: {admin_username}")
        print(f"   Mot de passe: admin123")
        print(f"   Email: admin@enseignement-sup.ga")
        
        print(f"\n🔐 Permissions:")
        print(f"   ✅ Superuser: Oui")
        print(f"   ✅ Staff: Oui")
        print(f"   ✅ Actif: Oui")
        
        print(f"\n🌐 Connectez-vous maintenant:")
        print(f"   1. Lancez: python manage.py runserver")
        print(f"   2. Allez sur: http://127.0.0.1:8000/login/")
        print(f"   3. Utilisez les identifiants ci-dessus")
    
    # Vérifier le nombre d'admins
    admin_count = User.objects.filter(is_staff=True).count()
    superuser_count = User.objects.filter(is_superuser=True).count()
    
    print(f"\n📊 Statistiques des administrateurs:")
    print(f"   Staff users: {admin_count}")
    print(f"   Superusers: {superuser_count}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
