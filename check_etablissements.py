#!/usr/bin/env python
"""
Script pour vérifier les établissements dans la base de données
"""

import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portail_enseignement.settings')
django.setup()

from core.models import Etablissement, Ville

def check_etablissements():
    """Vérifier les établissements dans la base de données"""
    
    print("🔍 Vérification des établissements dans la base de données...")
    
    # Compter les établissements
    total_etablissements = Etablissement.objects.count()
    print(f"\n📊 Total d'établissements: {total_etablissements}")
    
    if total_etablissements == 0:
        print("❌ Aucun établissement trouvé dans la base de données!")
        return
    
    # Lister tous les établissements
    print("\n📋 Liste des établissements:")
    for etablissement in Etablissement.objects.all():
        ville_nom = etablissement.ville.nom_ville if etablissement.ville else "❌ Pas de ville"
        print(f"   - {etablissement.nom_etab} ({ville_nom})")
    
    # Vérifier les villes
    print(f"\n🏙️ Total de villes: {Ville.objects.count()}")
    
    # Vérifier les établissements sans ville
    etablissements_sans_ville = Etablissement.objects.filter(ville__isnull=True)
    if etablissements_sans_ville.exists():
        print(f"\n⚠️ Établissements sans ville: {etablissements_sans_ville.count()}")
        for etablissement in etablissements_sans_ville:
            print(f"   - {etablissement.nom_etab}")

if __name__ == '__main__':
    check_etablissements()
