#!/usr/bin/env python
"""
Script pour mettre à jour les volumes horaires des matières
pour qu'ils soient cohérents (40, 30, 20 heures)
"""

import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portail_enseignement.settings')
django.setup()

from core.models import Matiere

def update_volumes_horaires():
    """Mettre à jour les volumes horaires des matières existantes"""
    
    # Mapping des volumes horaires par matière
    volumes_horaires = {
        'Mathématiques': 40,
        'Physique': 40,
        'Chimie': 30,
        'Biologie': 30,
        'Informatique': 40,
        'Économie': 30,
        'Droit Constitutionnel': 20,
        'Histoire': 20,
        'Anglais': 20,
        'Français': 20,
    }
    
    print("🔄 Mise à jour des volumes horaires...")
    
    updated_count = 0
    for matiere in Matiere.objects.all():
        if matiere.nom_matiere in volumes_horaires:
            nouveau_volume = volumes_horaires[matiere.nom_matiere]
            if matiere.volume_horaire != nouveau_volume:
                ancien_volume = matiere.volume_horaire
                matiere.volume_horaire = nouveau_volume
                matiere.save()
                print(f"✅ {matiere.nom_matiere}: {ancien_volume}h → {nouveau_volume}h")
                updated_count += 1
            else:
                print(f"⏭️ {matiere.nom_matiere}: déjà à {nouveau_volume}h")
        else:
            print(f"⚠️ {matiere.nom_matiere}: volume non défini")
    
    print(f"\n📊 Résumé:")
    print(f"   Matières mises à jour: {updated_count}")
    print(f"   Total matières: {Matiere.objects.count()}")
    
    # Vérification finale
    print(f"\n🔍 Vérification finale:")
    for matiere in Matiere.objects.all().order_by('nom_matiere'):
        print(f"   {matiere.nom_matiere}: {matiere.volume_horaire}h")

if __name__ == '__main__':
    update_volumes_horaires()
    print("\n✅ Mise à jour terminée !")
