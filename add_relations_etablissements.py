#!/usr/bin/env python
"""
Script pour ajouter des relations ManyToMany aux établissements existants
pour qu'ils aient des filières, matières et niveaux associés
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portail_enseignement.settings')
django.setup()

from core.models import Etablissement, Filiere, Matiere, Niveau

def add_relations_to_etablissements():
    """Ajouter des relations filières, matières et niveaux aux établissements existants"""
    
    print("🔗 Ajout des relations aux établissements...")
    
    # Récupérer tous les établissements
    etablissements = Etablissement.objects.all()
    filieres = list(Filiere.objects.all())
    matieres = list(Matiere.objects.all())
    niveaux = list(Niveau.objects.all())
    
    print(f"   - {etablissements.count()} établissements trouvés")
    print(f"   - {len(filieres)} filières disponibles")
    print(f"   - {len(matieres)} matières disponibles")
    print(f"   - {len(niveaux)} niveaux disponibles")
    
    # Pour chaque établissement, ajouter des relations
    for etablissement in etablissements:
        print(f"\n📚 Traitement de: {etablissement.nom_etab}")
        
        # Ajouter toutes les filières (chaque établissement offre toutes les filières)
        if filieres:
            etablissement.filieres.set(filieres)
            print(f"   ✅ {len(filieres)} filières ajoutées")
        
        # Ajouter toutes les matières (chaque établissement offre toutes les matières)
        if matieres:
            etablissement.matieres.set(matieres)
            print(f"   ✅ {len(matieres)} matières ajoutées")
        
        # Ajouter tous les niveaux (chaque établissement offre tous les niveaux)
        if niveaux:
            etablissement.niveaux.set(niveaux)
            print(f"   ✅ {len(niveaux)} niveaux ajoutés")
    
    print("\n✅ Relations ajoutées avec succès à tous les établissements!")

def verify_relations():
    """Vérifier que les relations ont bien été ajoutées"""
    print("\n🔍 Vérification des relations...")
    
    etablissements = Etablissement.objects.all()
    
    for etablissement in etablissements:
        print(f"\n📊 {etablissement.nom_etab}:")
        print(f"   - Filières: {etablissement.filieres.count()}")
        print(f"   - Matières: {etablissement.matieres.count()}")
        print(f"   - Niveaux: {etablissement.niveaux.count()}")
        
        # Afficher quelques exemples
        if etablissement.filieres.exists():
            premieres_filieres = etablissement.filieres.all()[:3]
            print(f"   - Exemples de filières: {', '.join([f.nom_filiere for f in premieres_filieres])}")
        
        if etablissement.matieres.exists():
            premieres_matieres = etablissement.matieres.all()[:3]
            print(f"   - Exemples de matières: {', '.join([m.nom_matiere for m in premieres_matieres])}")
        
        if etablissement.niveaux.exists():
            premiers_niveaux = etablissement.niveaux.all()[:3]
            print(f"   - Exemples de niveaux: {', '.join([n.nom_niveau for n in premiers_niveaux])}")

if __name__ == '__main__':
    print("=" * 60)
    print("🔗 AJOUT DES RELATIONS AUX ÉTABLISSEMENTS")
    print("=" * 60)
    
    try:
        add_relations_to_etablissements()
        verify_relations()
        
        print("\n" + "=" * 60)
        print("✅ Opération terminée avec succès!")
        print("   Tous les établissements ont maintenant des filières,")
        print("   matières et niveaux associés.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        print("   Vérifiez que les modèles ont les champs ManyToMany nécessaires")
