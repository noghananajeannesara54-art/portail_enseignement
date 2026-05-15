#!/usr/bin/env python
import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portail_enseignement.settings')
django.setup()

from core.models import Matiere, Etablissement, Filiere, Niveau, SupportCours

def check_matiere_algorithmique():
    """Vérifier où se trouve la matière Algorithmique"""
    
    print("=" * 60)
    print("VÉRIFICATION DE LA MATIÈRE ALGORITHMIQUE")
    print("=" * 60)
    
    # 1. Chercher la matière Algorithmique
    matieres_algo = Matiere.objects.filter(nom_matiere__icontains='algorithm')
    print(f"\n📚 Matières contenant 'algorithm': {matieres_algo.count()}")
    
    for matiere in matieres_algo:
        print(f"  - ID: {matiere.pk}, Nom: {matiere.nom_matiere}, Code: {matiere.code_matiere}")
        
        # 2. Vérifier les supports de cours pour cette matière
        supports = SupportCours.objects.filter(matiere=matiere)
        print(f"    📄 Supports de cours: {supports.count()}")
        for support in supports:
            print(f"      - {support.titre or 'Sans titre'} (enseignant: {support.enseignant})")
        
        # 3. Vérifier les établissements qui ont cette matière
        etablissements_avec_matiere = Etablissement.objects.filter(matieres=matiere)
        print(f"    🏫 Établissements avec cette matière: {etablissements_avec_matiere.count()}")
        for etab in etablissements_avec_matiere:
            print(f"      - {etab.nom_etab} (ville: {etab.ville})")
    
    # 4. Vérifier toutes les matières existantes
    print(f"\n📋 Toutes les matières dans la base: {Matiere.objects.count()}")
    for matiere in Matiere.objects.all():
        print(f"  - {matiere.nom_matiere} (ID: {matiere.pk})")
    
    # 5. Vérifier les matières par établissement
    print(f"\n🏫 Matières par établissement:")
    for etab in Etablissement.objects.all()[:5]:  # Limiter à 5 pour la lisibilité
        matieres = etab.matieres.all()
        print(f"  {etab.nom_etab}: {matieres.count()} matières")
        for matiere in matieres:
            print(f"    - {matiere.nom_matiere}")
    
    # 6. Vérifier les filières et leurs matières associées
    print(f"\n🎓 Filières et matières:")
    for filiere in Filiere.objects.all():
        print(f"  {filiere.nom_filiere}:")
        # Chercher les matières qui correspondent à cette filière
        matieres_correspondantes = []
        for matiere in Matiere.objects.all():
            if any(keyword.lower() in matiere.nom_matiere.lower() 
                   for keyword in filiere.nom_filiere.lower().split()):
                matieres_correspondantes.append(matiere)
        
        for matiere in matieres_correspondantes[:3]:  # Limiter à 3 pour la lisibilité
            print(f"    - {matiere.nom_matiere}")

if __name__ == "__main__":
    check_matiere_algorithmique()
