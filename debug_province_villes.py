#!/usr/bin/env python
"""
Script pour diagnostiquer les relations provinces-villes
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
    
    from core.models import Province, Ville, Etablissement
    
    print("=== DIAGNOSTIC PROVINCES-VILLES ===")
    
    # Vérifier toutes les provinces
    provinces = Province.objects.all()
    print(f"\n📊 Provinces: {provinces.count()}")
    
    for province in provinces:
        print(f"\n🏛️ Province: {province.nom_province} (ID: {province.pk})")
        
        # Vérifier les villes liées
        villes = province.villes.all()
        print(f"   📊 Villes liées: {villes.count()}")
        
        if villes.exists():
            for ville in villes:
                etablissements = ville.etablissements.all()
                print(f"      🏙️ {ville.nom_ville} (ID: {ville.pk}) - {etablissements.count()} établissements")
                
                if etablissements.exists():
                    for etab in etablissements[:3]:  # Limiter à 3 pour l'affichage
                        print(f"         🏫 {etab.nom_etab}")
        else:
            print("      ❌ Aucune ville liée!")
    
    # Vérifier toutes les villes sans province
    print(f"\n🔍 Vérification des villes orphelines...")
    all_villes = Ville.objects.all()
    villes_sans_province = all_villes.filter(province__isnull=True)
    
    if villes_sans_province.exists():
        print(f"❌ {villes_sans_province.count()} villes sans province:")
        for ville in villes_sans_province:
            print(f"   🏙️ {ville.nom_ville} (ID: {ville.pk})")
    else:
        print("✅ Toutes les villes ont une province")
    
    # Statistiques finales
    print(f"\n📊 Résumé:")
    print(f"   Provinces: {Province.objects.count()}")
    print(f"   Villes totales: {Ville.objects.count()}")
    print(f"   Villes liées: {Ville.objects.filter(province__isnull=False).count()}")
    print(f"   Villes orphelines: {villes_sans_province.count()}")
    print(f"   Établissements: {Etablissement.objects.count()}")
    
    # Vérifier les établissements sans ville
    etabs_sans_ville = Etablissement.objects.filter(ville__isnull=True)
    if etabs_sans_ville.exists():
        print(f"\n❌ {etabs_sans_ville.count()} établissements sans ville:")
        for etab in etabs_sans_ville:
            print(f"   🏫 {etab.nom_etab}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
