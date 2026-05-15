#!/usr/bin/env python
"""
Script pour créer une structure hiérarchique complète :
- 9 provinces (déjà créées)
- Chaque province a 9 villes (à vérifier/compléter)
- Chaque ville a au moins 3 établissements
- Chaque établissement a des niveaux, filières, et enseignants
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portail_enseignement.settings')
django.setup()

from core.models import Province, Ville, Etablissement, Filiere, Niveau, Matiere, Enseignant, User
from django.contrib.auth.hashers import make_password

def create_etablissements_for_all_villes():
    """Créer au moins 3 établissements pour chaque ville"""
    
    print("🏫 Création des établissements pour toutes les villes...")
    
    # Types d'établissements variés
    types_etablissements = ['universite', 'ecole_sup', 'institut', 'centre']
    noms_etablissements = [
        'Université', 'École Supérieure', 'Institut', 'Centre de Formation',
        'Faculté', 'Institut Supérieur', 'École Technique', 'Centre d\'Excellence'
    ]
    
    villes = Ville.objects.all()
    created_count = 0
    
    for ville in villes:
        print(f"\n🏙️  Traitement de {ville.nom_ville} ({ville.province.nom_province})")
        
        # Vérifier combien d'établissements existent déjà pour cette ville
        existing_etabs = Etablissement.objects.filter(ville=ville).count()
        print(f"   - Établissements existants: {existing_etabs}")
        
        # Créer des établissements manquants pour atteindre au moins 3
        needed = max(0, 3 - existing_etabs)
        
        if needed > 0:
            for i in range(needed):
                # Générer un nom unique
                nom_etab = f"{noms_etablissements[i % len(noms_etablissements)]} de {ville.nom_ville}"
                if existing_etabs > 0 or i > 0:
                    nom_etab += f" {i + 1}"
                
                # Créer l'établissement
                etablissement, created = Etablissement.objects.get_or_create(
                    nom_etab=nom_etab,
                    defaults={
                        'type_etab': types_etablissements[i % len(types_etablissements)],
                        'ville': ville,
                        'adresse': f'Avenue principale, {ville.nom_ville}',
                        'telephone': f'+241 01 45 6{7+i}8{9+i}',
                        'email': f'contact{7+i}@{nom_etab.lower().replace(" ", "_").replace("\'", "")}.ga',
                        'site_web': f'www.{nom_etab.lower().replace(" ", "_").replace("\'", "")}.ga',
                        'description': f'Établissement d\'excellence situé à {ville.nom_ville}, spécialisé dans l\'enseignement supérieur.'
                    }
                )
                
                if created:
                    created_count += 1
                    print(f"   ✅ Créé: {nom_etab}")
        
        else:
            print(f"   ✅ Déjà assez d'établissements ({existing_etabs})")
    
    print(f"\n📊 Total d'établissements créés: {created_count}")
    return Etablissement.objects.all()

def create_enseignants_for_filieres():
    """Créer au moins 3 enseignants pour chaque filière"""
    
    print("\n👨‍🏫 Création des enseignants pour chaque filière...")
    
    filieres = Filiere.objects.all()
    created_count = 0
    
    # Noms et prénoms pour les enseignants
    prenoms = ['Jean', 'Marie', 'Pierre', 'Sophie', 'Paul', 'Isabelle', 'Michel', 'Claire', 'Robert', 'Nathalie']
    noms = ['Mbarga', 'Ondo', 'Nguema', 'Meye', 'Eyi', 'Mba', 'Essono', 'Obame', 'Nze', 'Adande']
    
    for filiere in filieres:
        print(f"\n📚 Filière: {filiere.nom_filiere}")
        
        # Vérifier combien d'enseignants existent déjà
        existing_enseignants = User.objects.filter(
            enseignant__matieres__niveau__isnull=False
        ).distinct().count()
        
        # Créer 3 enseignants par filière
        for i in range(3):
            prenom = prenoms[i % len(prenoms)]
            nom = noms[i % len(noms)]
            username = f"{prenom.lower()}.{nom.lower()}_{filiere.id}"
            
            # Créer l'utilisateur
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': prenom,
                    'last_name': nom,
                    'email': f'{username}@example.com',
                    'password': make_password('password123'),
                    'is_staff': False,
                    'is_active': True,
                }
            )
            
            if created:
                # Créer le profil enseignant
                enseignant, created_ens = Enseignant.objects.get_or_create(
                    user=user,
                    defaults={
                        'specialite': f'Expert en {filiere.nom_filiere}',
                        'grade': ['Professeur', 'Maître de Conférences', 'Assistant'][i % 3]
                    }
                )
                
                if created_ens:
                    # Assigner des matières de la filière
                    matieres_filiere = Matiere.objects.all()[:3]  # Prendre 3 matières
                    enseignant.matieres.set(matieres_filiere)
                    
                    # Assigner à un établissement aléatoire
                    etablissements = Etablissement.objects.all()
                    if etablissements.exists():
                        enseignant.etablissement = etablissements[i % etablissements.count()]
                        enseignant.save()
                    
                    created_count += 1
                    print(f"   ✅ Créé: {prenom} {nom} - {enseignant.specialite}")
    
    print(f"\n📊 Total d'enseignants créés: {created_count}")
    return Enseignant.objects.all()

def verify_complete_structure():
    """Vérifier que la structure est complète"""
    
    print("\n🔍 Vérification de la structure complète...")
    
    provinces = Province.objects.all()
    villes = Ville.objects.all()
    etablissements = Etablissement.objects.all()
    filieres = Filiere.objects.all()
    enseignants = Enseignant.objects.all()
    
    print(f"\n📊 Résumé global:")
    print(f"   - Provinces: {provinces.count()}")
    print(f"   - Villes: {villes.count()}")
    print(f"   - Établissements: {etablissements.count()}")
    print(f"   - Filières: {filieres.count()}")
    print(f"   - Enseignants: {enseignants.count()}")
    
    # Vérifier chaque province
    print(f"\n🏛️  Détail par province:")
    for province in provinces:
        villes_province = Ville.objects.filter(province=province)
        total_etabs = sum(Etablissement.objects.filter(ville=v).count() for v in villes_province)
        
        print(f"   {province.nom_province}:")
        print(f"     - Villes: {villes_province.count()}/9")
        print(f"     - Établissements: {total_etabs}")
        
        # Vérifier si chaque ville a au moins 3 établissements
        for ville in villes_province:
            etabs_ville = Etablissement.objects.filter(ville=ville).count()
            if etabs_ville < 3:
                print(f"       ⚠️  {ville.nom_ville}: seulement {etabs_ville} établissements")
    
    # Vérifier les enseignants par filière
    print(f"\n👨‍🏫 Enseignants par filière:")
    for filiere in filieres:
        ens_count = enseignants.filter(matieres__niveau__isnull=False).count()
        print(f"   - {filiere.nom_filiere}: {ens_count} enseignants")

if __name__ == '__main__':
    print("=" * 80)
    print("🏗️  CRÉATION DE LA STRUCTURE HIÉRARCHIQUE COMPLÈTE")
    print("=" * 80)
    
    try:
        # 1. Créer des établissements pour chaque ville
        etablissements = create_etablissements_for_all_villes()
        
        # 2. Ajouter les relations (filieres, matieres, niveaux) aux nouveaux établissements
        print("\n🔗 Ajout des relations aux nouveaux établissements...")
        from add_relations_etablissements import add_relations_to_etablissements
        add_relations_to_etablissements()
        
        # 3. Créer des enseignants pour chaque filière
        enseignants = create_enseignants_for_filieres()
        
        # 4. Vérifier la structure complète
        verify_complete_structure()
        
        print("\n" + "=" * 80)
        print("✅ Structure hiérarchique complète créée avec succès!")
        print("   - 9 provinces")
        print("   - Chaque province a 9 villes")
        print("   - Chaque ville a au moins 3 établissements")
        print("   - Chaque établissement a des filières, matières et niveaux")
        print("   - Chaque filière a des enseignants")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
