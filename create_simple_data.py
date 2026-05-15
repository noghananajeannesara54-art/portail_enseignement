#!/usr/bin/env python
import os
import sys
import django

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portail_enseignement.settings')
django.setup()

from core.models import Province, Ville, Etablissement, Filiere, Matiere, Enseignant, SupportCours, Niveau
from django.contrib.auth.models import User

def create_provinces():
    """Créer les 9 provinces du Gabon"""
    provinces_data = [
        {'nom_province': 'Estuaire', 'code_province': 'EST'},
        {'nom_province': 'Haut-Ogooué', 'code_province': 'HO'},
        {'nom_province': 'Moyen-Ogooué', 'code_province': 'MO'},
        {'nom_province': 'Ngounié', 'code_province': 'NG'},
        {'nom_province': 'Nyanga', 'code_province': 'NY'},
        {'nom_province': 'Ogooué-Ivindo', 'code_province': 'OI'},
        {'nom_province': 'Ogooué-Lolo', 'code_province': 'OL'},
        {'nom_province': 'Ogooué-Maritime', 'code_province': 'OM'},
        {'nom_province': 'Woleu-Ntem', 'code_province': 'WN'},
    ]
    
    created_provinces = []
    for province_data in provinces_data:
        province, created = Province.objects.get_or_create(
            nom_province=province_data['nom_province'],
            defaults={'code_province': province_data['code_province']}
        )
        created_provinces.append(province)
        if created:
            print(f"✅ Province créée: {province.nom_province}")
    
    return created_provinces

def create_villes(provinces):
    """Créer des villes pour chaque province"""
    villes_data = {
        'Estuaire': ['Libreville', 'Owendo', 'Ntoum'],
        'Haut-Ogooué': ['Franceville', 'Moanda', 'Mounana'],
        'Moyen-Ogooué': ['Lambaréné', 'Mouila', 'Ndjolé'],
        'Ngounié': ['Mouila', 'Fougamou', 'Ndendé'],
        'Nyanga': ['Tchibanga', 'Mayumba', 'Moungoundou'],
        'Ogooué-Ivindo': ['Makokou', 'Mékambo', 'Booué'],
        'Ogooué-Lolo': ['Koulamoutou', 'Lastoursville', 'Poubara'],
        'Ogooué-Maritime': ['Port-Gentil', 'Omboué', 'Gamba'],
        'Woleu-Ntem': ['Oyem', 'Bitam', 'Mitzic'],
    }
    
    created_villes = []
    for province in provinces:
        if province.nom_province in villes_data:
            for nom_ville in villes_data[province.nom_province]:
                ville, created = Ville.objects.get_or_create(
                    nom_ville=nom_ville,
                    province=province
                )
                created_villes.append(ville)
                if created:
                    print(f"✅ Ville créée: {ville.nom_ville} ({province.nom_province})")
    
    return created_villes

def create_filieres():
    """Créer 3 filières principales"""
    filieres_data = [
        {'nom_filiere': 'Informatique', 'description': 'Études en sciences informatiques et programmation'},
        {'nom_filiere': 'Gestion', 'description': 'Sciences de gestion et administration des entreprises'},
        {'nom_filiere': 'Droit', 'description': 'Droit public et droit privé'},
    ]
    
    created_filieres = []
    for filiere_data in filieres_data:
        filiere, created = Filiere.objects.get_or_create(
            nom_filiere=filiere_data['nom_filiere'],
            defaults={'description': filiere_data['description']}
        )
        created_filieres.append(filiere)
        if created:
            print(f"✅ Filière créée: {filiere.nom_filiere}")
    
    return created_filieres

def create_niveaux():
    """Créer 3 niveaux principaux"""
    niveaux_data = [
        {'nom_niveau': 'Licence 1', 'code_niveau': 'L1'},
        {'nom_niveau': 'Licence 2', 'code_niveau': 'L2'},
        {'nom_niveau': 'Licence 3', 'code_niveau': 'L3'},
    ]
    
    created_niveaux = []
    for niveau_data in niveaux_data:
        niveau, created = Niveau.objects.get_or_create(
            nom_niveau=niveau_data['nom_niveau'],
            defaults={'code_niveau': niveau_data['code_niveau']}
        )
        created_niveaux.append(niveau)
        if created:
            print(f"✅ Niveau créé: {niveau.nom_niveau}")
    
    return created_niveaux

def create_matieres(niveaux):
    """Créer 3 matières par niveau"""
    matieres_data = {
        'Licence 1': ['Mathématiques', 'Informatique', 'Introduction au Droit'],
        'Licence 2': ['Algorithmique', 'Comptabilité', 'Droit Civil'],
        'Licence 3': ['Bases de données', 'Finance', 'Droit des Affaires'],
    }
    
    created_matieres = []
    for niveau in niveaux:
        if niveau.nom_niveau in matieres_data:
            for nom_matiere in matieres_data[niveau.nom_niveau]:
                matiere, created = Matiere.objects.get_or_create(
                    nom_matiere=nom_matiere,
                    defaults={
                        'code_matiere': nom_matiere[:8].upper(),
                        'niveau': niveau,
                        'volume_horaire': 45
                    }
                )
                created_matieres.append(matiere)
                if created:
                    print(f"✅ Matière créée: {matiere.nom_matiere} ({niveau.nom_niveau})")
    
    return created_matieres

def create_etablissements(villes):
    """Créer 3 établissements principaux"""
    etablissements_data = [
        {
            'nom_etab': 'Université Omar Bongo Ondimba',
            'type_etab': 'universite',
            'ville': 'Libreville',
            'adresse': 'Avenue Omar Bongo, Libreville',
            'telephone': '+241 01 45 67 89',
            'email': 'contact@uob.ga',
        },
        {
            'nom_etab': 'Université des Sciences et Techniques de Masuku',
            'type_etab': 'universite',
            'ville': 'Franceville',
            'adresse': 'Campus de Masuku, Franceville',
            'telephone': '+241 01 45 67 90',
            'email': 'info@ustm.ga',
        },
        {
            'nom_etab': 'Institut National des Sciences de Gestion',
            'type_etab': 'institut',
            'ville': 'Port-Gentil',
            'adresse': 'Boulevard Triomphal, Port-Gentil',
            'telephone': '+241 01 45 67 92',
            'email': 'info@insg.ga',
        },
    ]
    
    created_etablissements = []
    for etablissement_data in etablissements_data:
        # Trouver la ville
        ville_obj = None
        for ville in villes:
            if ville.nom_ville == etablissement_data['ville']:
                ville_obj = ville
                break
        
        if ville_obj:
            etablissement, created = Etablissement.objects.get_or_create(
                nom_etab=etablissement_data['nom_etab'],
                defaults={
                    'type_etab': etablissement_data['type_etab'],
                    'ville': ville_obj,
                    'adresse': etablissement_data['adresse'],
                    'telephone': etablissement_data['telephone'],
                    'email': etablissement_data['email'],
                }
            )
            created_etablissements.append(etablissement)
            if created:
                print(f"✅ Établissement créé: {etablissement.nom_etab} à {ville_obj.nom_ville}")
    
    return created_etablissements

def create_users():
    """Créer seulement l'utilisateur admin"""
    user_data = {
        'username': 'admin',
        'email': 'admin@gabon.edu',
        'first_name': 'Admin',
        'last_name': 'System',
        'is_staff': True,
        'is_superuser': True,
    }
    
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'is_staff': user_data['is_staff'],
            'is_superuser': user_data['is_superuser'],
        }
    )
    if created:
        user.set_password('password123')
        user.save()
        print(f"✅ Utilisateur admin créé: {user.username}")
    else:
        print(f"ℹ️  Utilisateur admin existe déjà: {user.username}")
    
    return [user]

def main():
    """Fonction principale pour créer les données simplifiées"""
    print("🚀 Création des données simplifiées...")
    print("=" * 50)
    
    # 1. Créer les provinces
    print("\n📍 Création des provinces...")
    provinces = create_provinces()
    
    # 2. Créer les villes
    print("\n🏙️  Création des villes...")
    villes = create_villes(provinces)
    
    # 3. Créer les filières
    print("\n📚 Création des filières...")
    filieres = create_filieres()
    
    # 4. Créer les niveaux
    print("\n📋 Création des niveaux...")
    niveaux = create_niveaux()
    
    # 5. Créer les matières
    print("\n📖 Création des matières...")
    matieres = create_matieres(niveaux)
    
    # 6. Créer les établissements
    print("\n🏫 Création des établissements...")
    etablissements = create_etablissements(villes)
    
    # 7. Créer les utilisateurs
    print("\n👥 Création des utilisateurs...")
    users = create_users()
    
    print("\n" + "=" * 50)
    print("✅ Données simplifiées créées avec succès !")
    print(f"📊 Résumé:")
    print(f"   - Provinces: {Province.objects.count()} (complètes)")
    print(f"   - Villes: {Ville.objects.count()} (3 par province)")
    print(f"   - Filières: {Filiere.objects.count()} (principales)")
    print(f"   - Niveaux: {Niveau.objects.count()} (Licence 1-3)")
    print(f"   - Matières: {Matiere.objects.count()} (3 par niveau)")
    print(f"   - Établissements: {Etablissement.objects.count()} (principaux)")
    print(f"   - Utilisateurs: {User.objects.count()} (essentiels)")
    print("\n🔑 Identifiant de connexion:")
    print("   - Admin: admin / password123")
    print("\n💡 L'administrateur pourra ajouter d'autres utilisateurs et données via l'interface Django Admin")

if __name__ == '__main__':
    main()
