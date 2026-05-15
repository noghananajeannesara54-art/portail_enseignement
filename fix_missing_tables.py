#!/usr/bin/env python
"""
Script pour créer les tables Django manquantes
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
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'core',
        ],
        SECRET_KEY='temp-key',
        USE_TZ=False,
    )
    
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.db import connection
    
    print("=== CRÉATION TABLES DJANGO MANQUANTES ===")
    
    # Vérifier les tables existantes
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in cursor.fetchall()]
    
    print(f"\n📊 Tables existantes: {len(existing_tables)}")
    
    # Tables Django essentielles manquantes
    required_tables = [
        'django_migrations',
        'django_content_type',
        'auth_permission',
        'auth_user',
        'auth_group',
        'auth_user_groups',
        'django_session',
        'auth_group_permissions',
        'auth_user_user_permissions'
    ]
    
    missing_tables = [table for table in required_tables if table not in existing_tables]
    
    if missing_tables:
        print(f"\n❌ Tables manquantes: {len(missing_tables)}")
        for table in missing_tables:
            print(f"   - {table}")
        
        print(f"\n🔧 Exécution des migrations pour créer les tables manquantes...")
        
        # Exécuter les migrations
        try:
            execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
            print(f"✅ Migrations exécutées avec succès!")
        except Exception as e:
            print(f"⚠️ Erreur lors des migrations: {e}")
            print(f"🔧 Tentative de création manuelle...")
            
            # Création manuelle des tables critiques
            with connection.cursor() as cursor:
                # Désactiver les contraintes
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                
                # Table django_session
                if 'django_session' in missing_tables:
                    try:
                        cursor.execute("""
                            CREATE TABLE django_session (
                                session_key varchar(40) NOT NULL PRIMARY KEY,
                                session_data longtext NOT NULL,
                                expire_date datetime NOT NULL
                            )
                        """)
                        print(f"✅ Table django_session créée")
                    except Exception as e:
                        print(f"❌ Erreur création django_session: {e}")
                
                # Table auth_user
                if 'auth_user' in missing_tables:
                    try:
                        cursor.execute("""
                            CREATE TABLE auth_user (
                                id int AUTO_INCREMENT NOT NULL PRIMARY KEY,
                                password varchar(128) NOT NULL,
                                last_login datetime,
                                is_superuser bool NOT NULL,
                                username varchar(150) NOT NULL UNIQUE,
                                first_name varchar(150) NOT NULL,
                                last_name varchar(150) NOT NULL,
                                email varchar(254) NOT NULL,
                                is_staff bool NOT NULL,
                                is_active bool NOT NULL,
                                date_joined datetime NOT NULL
                            )
                        """)
                        print(f"✅ Table auth_user créée")
                    except Exception as e:
                        print(f"❌ Erreur création auth_user: {e}")
                
                # Réactiver les contraintes
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Vérification finale
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            final_tables = [table[0] for table in cursor.fetchall()]
        
        print(f"\n📊 Tables finales: {len(final_tables)}")
        
        # Vérifier les tables essentielles
        essential_present = [table for table in required_tables if table in final_tables]
        essential_missing = [table for table in required_tables if table not in final_tables]
        
        print(f"✅ Tables essentielles présentes: {len(essential_present)}")
        print(f"❌ Tables essentielles manquantes: {len(essential_missing)}")
        
        if essential_missing:
            print(f"\n⚠️ Tables encore manquantes:")
            for table in essential_missing:
                print(f"   - {table}")
        else:
            print(f"\n🎉 Toutes les tables essentielles sont présentes!")
            print(f"\n🌐 Vous pouvez maintenant vous connecter!")
            print(f"   python manage.py runserver")
            print(f"   http://127.0.0.1:8000/login/")
    
    else:
        print(f"\n✅ Toutes les tables Django sont déjà présentes!")
        print(f"\n🌐 Le problème vient d'ailleurs. Vérifiez:")
        print(f"   1. Les permissions de la base")
        print(f"   2. La configuration MySQL")
        print(f"   3. Le serveur MySQL")

except Exception as e:
    print(f"❌ Erreur générale: {e}")
    import traceback
    traceback.print_exc()
