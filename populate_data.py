#!/usr/bin/env python
"""
Script pour peupler la base de données avec les données initiales
du portail d'enseignement supérieur du Gabon
"""

import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portail_enseignement.settings')
django.setup()

from core.models import Province, Ville, Etablissement, Filiere, Niveau, Matiere

def create_provinces():
    """Créer les provinces du Gabon"""
    provinces_data = [
        ('Estuaire', 'EST', 'Province côtière avec la capitale Libreville, centre économique et politique du Gabon'),
        ('Haut-Ogooué', 'HO', 'Province riche en ressources minières, avec la ville de Franceville'),
        ('Moyen-Ogooué', 'MO', 'Province forestière avec la ville de Lambaréné'),
        ('Ngounié', 'NG', 'Province agricole divisée en Ngounié-I et Ngounié-II'),
        ('Nyanga', 'NY', 'Province méridionale connue pour ses plages et le Parc National de Moukalaba-Doudou'),
        ('Ogooué-Lolo', 'OL', 'Province traversée par le fleuve Ogooué-Lolo'),
        ('Ogooué-Ivindo', 'OI', 'Province la plus vaste du Gabon, riche en ressources forestières'),
        ('Ogooué-Maritime', 'OM', 'Province côtière avec Port-Gentil, centre pétrolier'),
        ('Woleu-Ntem', 'WN', 'Province frontalière avec le Cameroun et la Guinée Équatoriale'),
    ]
    
    created_provinces = []
    for nom, code, description in provinces_data:
        province, created = Province.objects.get_or_create(
            nom_province=nom,
            defaults={
                'code_province': code,
                'description': description
            }
        )
        created_provinces.append(province)
        print(f"Province {'créée' if created else 'existante'}: {nom}")
    
    return created_provinces

def create_villes(provinces):
    """Créer les villes principales"""
    villes_data = [
        # Estuaire
        ('Libreville', provinces[0], 'Capitale politique et économique du Gabon'),
        ('Owendo', provinces[0], 'Ville côtière près de Libreville'),
        ('Ntoum', provinces[0], 'Ville de la province de l\'Estuaire'),
        # Haut-Ogooué
        ('Franceville', provinces[1], 'Chef-lieu de la province du Haut-Ogooué'),
        ('Mounana', provinces[1], 'Ville minière de la province du Haut-Ogooué'),
        ('Makokou', provinces[1], 'Ville industrielle du Haut-Ogooué'),
        # Moyen-Ogooué
        ('Lambaréné', provinces[2], 'Chef-lieu de la province du Moyen-Ogooué'),
        ('Ndjolé', provinces[2], 'Ville fluviale du Moyen-Ogooué'),
        # Ngounié
        ('Fougamou', provinces[3], 'Chef-lieu de la province de la Ngounié'),
        ('Mbigou', provinces[3], 'Ville de la province de la Ngounié'),
        # Nyanga
        ('Tchibanga', provinces[4], 'Chef-lieu de la province de la Nyanga'),
        ('Moukalaba-Doudou', provinces[4], 'Ville côtière de la province de la Nyanga'),
        # Ogooué-Lolo
        ('Koulamoutou', provinces[5], 'Chef-lieu de la province de l\'Ogooué-Lolo'),
        ('Lastourville', provinces[5], 'Ville de la province de l\'Ogooué-Lolo'),
        # Ogooué-Ivindo
        ('Mékambo', provinces[6], 'Ville forestière de la province de l\'Ogooué-Ivindo'),
        # Ogooué-Maritime
        ('Port-Gentil', provinces[7], 'Chef-lieu de la province de l\'Ogooué-Maritime, centre pétrolier'),
        ('Omboué', provinces[7], 'Ville côtière de la province de l\'Ogooué-Maritime'),
        # Woleu-Ntem
        ('Oyem', provinces[8], 'Chef-lieu de la province du Woleu-Ntem'),
        ('Bitam', provinces[8], 'Ville frontalière de la province du Woleu-Ntem'),
    ]
    
    created_villes = []
    for nom, province, description in villes_data:
        ville, created = Ville.objects.get_or_create(
            nom_ville=nom,
            province=province,
            defaults={'description': description}
        )
        created_villes.append(ville)
        print(f"Ville {'créée' if created else 'existante'}: {nom}")
    
    return created_villes

def create_filieres(etablissements):
    """Créer les filières d'études"""
    filieres_data = [
        ('Sciences Exactes', 'SCI', 'Mathématiques, Physique, Chimie, Sciences de la Vie et de la Terre', etablissements[0]),
        ('Sciences Humaines', 'SHS', 'Histoire, Géographie, Philosophie, Langues et Littératures', etablissements[0]),
        ('Sciences Économiques', 'SEC', 'Économie, Gestion, Commerce, Finance', etablissements[0]),
        ('Droit et Sciences Politiques', 'DSP', 'Droit public, privé, international, relations internationales', etablissements[0]),
        ('Médecine et Sciences de la Santé', 'MED', 'Médecine générale, pharmacie, chirurgie, santé publique', etablissements[2]),
        ('Ingénierie et Technologie', 'ING', 'Génie civil, informatique, télécommunications, énergies', etablissements[1]),
        ('Agronomie et Sciences Forestières', 'AGR', 'Agriculture, agro-industrie, foresterie, environnement', etablissements[1]),
        ('Arts et Culture', 'ART', 'Arts plastiques, musique, théâtre, cinéma, patrimoine culturel', etablissements[0]),
        ('Éducation Physique et Sport', 'EPS', 'Éducation physique, sport, kinésithérapie, ergothérapie', etablissements[2]),
        ('Communication et Journalisme', 'COM', 'Journalisme, communication publique, relations publiques, marketing', etablissements[0]),
    ]
    
    created_filieres = []
    for nom, code, description, etablissement in filieres_data:
        filiere, created = Filiere.objects.get_or_create(
            nom_filiere=nom,
            etablissement=etablissement,
            defaults={
                'code_filiere': code,
                'description': description
            }
        )
        created_filieres.append(filiere)
        print(f"Filière {'créée' if created else 'existante'}: {nom}")
    
    return created_filieres

def create_niveaux(filieres):
    """Créer les niveaux académiques"""
    niveaux_data = [
        ('L1', 'Licence 1', filieres[0]),
        ('L2', 'Licence 2', filieres[0]),
        ('L3', 'Licence 3', filieres[0]),
        ('M1', 'Master 1', filieres[0]),
        ('M2', 'Master 2', filieres[0]),
    ]
    
    created_niveaux = []
    for code, description, filiere in niveaux_data:
        niveau, created = Niveau.objects.get_or_create(
            libelle_niveau=code,
            filiere=filiere,
            defaults={'description': description}
        )
        created_niveaux.append(niveau)
        print(f"Niveau {'créé' if created else 'existant'}: {code} - {description}")
    
    return created_niveaux

def create_matieres(niveaux):
    """Créer les matières"""
    matieres_data = [
        ('Mathématiques', 'MAT', 'Algèbre, analyse, géométrie, probabilités', 40.00, niveaux[0]),
        ('Physique', 'PHY', 'Mécanique, électricité, optique, thermodynamique', 40.00, niveaux[0]),
        ('Chimie', 'CHI', 'Chimie organique, minérale, analytique', 30.00, niveaux[0]),
        ('Biologie', 'BIO', 'Biologie cellulaire, moléculaire, écologie', 30.00, niveaux[0]),
        ('Informatique', 'INF', 'Algorithmique, programmation, bases de données', 40.00, niveaux[0]),
        ('Économie', 'ECO', 'Microéconomie, macroéconomie, économétrie', 30.00, niveaux[1]),
        ('Droit Constitutionnel', 'DRC', 'Droit constitutionnel gabonais et comparé', 20.00, niveaux[1]),
        ('Histoire', 'HIS', 'Histoire du Gabon, histoire contemporaine', 20.00, niveaux[1]),
        ('Anglais', 'ANG', 'Grammaire, littérature, traduction', 20.00, niveaux[2]),
        ('Français', 'FRA', 'Littérature française, linguistique, expression écrite', 20.00, niveaux[2]),
    ]
    
    created_matieres = []
    for nom, code, description, volume, niveau in matieres_data:
        matiere, created = Matiere.objects.get_or_create(
            nom_matiere=nom,
            niveau=niveau,
            defaults={
                'code_matiere': code,
                'description': description,
                'volume_horaire': volume
            }
        )
        created_matieres.append(matiere)
        print(f"Matière {'créée' if created else 'existante'}: {nom}")
    
    return created_matieres

def create_etablissements(villes):
    """Créer quelques établissements exemples"""
    etablissements_data = [
        ('Université Omar Bongo', villes[0], 'public', 'Avenue Omar Bongo, Libreville', '+241 01 73 45 67', 'info@uo.ga'),
        ('Université des Sciences et Techniques', villes[3], 'public', 'BP 1234, Franceville', '+241 01 73 45 68', 'info@ust.ga'),
        ('École Normale Supérieure', villes[0], 'public', 'Avenue de l\'Éducation, Libreville', '+241 01 73 45 69', 'info@ens.ga'),
        ('Institut National de Polytechnique', villes[14], 'public', 'Zone Industrielle, Port-Gentil', '+241 01 73 45 70', 'info@inp.ga'),
        ('Université de Ntoum', villes[2], 'public', 'Route Nationale 1, Ntoum', '+241 01 73 45 71', 'info@un.ga'),
    ]
    
    created_etablissements = []
    for nom, ville, type_etab, adresse, tel, email in etablissements_data:
        etablissement, created = Etablissement.objects.get_or_create(
            nom_etab=nom,
            defaults={
                'ville': ville,
                'type_etab': type_etab,
                'adresse': adresse,
                'telephone': tel,
                'email': email,
                'description': f'Établissement {type_etab} d\'enseignement supérieur situé à {ville.nom_ville}'
            }
        )
        created_etablissements.append(etablissement)
        print(f"Établissement {'créé' if created else 'existant'}: {nom}")
    
    return created_etablissements

def main():
    """Fonction principale pour peupler la base de données"""
    print("🚀 Début du peuplement de la base de données...")
    
    # Créer les provinces
    print("\n📍 Création des provinces...")
    provinces = create_provinces()
    
    # Créer les villes
    print("\n🏙️ Création des villes...")
    villes = create_villes(provinces)
    
    # Créer les établissements
    print("\n🏫 Création des établissements...")
    etablissements = create_etablissements(villes)
    
    # Créer les filières
    print("\n📚 Création des filières...")
    filieres = create_filieres(etablissements)
    
    # Créer les niveaux
    print("\n🎓 Création des niveaux...")
    niveaux = create_niveaux(filieres)
    
    # Créer les matières
    print("\n📖 Création des matières...")
    matieres = create_matieres(niveaux)
    
    # Statistiques finales
    print("\n📊 Statistiques finales:")
    print(f"   Provinces: {Province.objects.count()}")
    print(f"   Villes: {Ville.objects.count()}")
    print(f"   Établissements: {Etablissement.objects.count()}")
    print(f"   Filières: {Filiere.objects.count()}")
    print(f"   Niveaux: {Niveau.objects.count()}")
    print(f"   Matières: {Matiere.objects.count()}")
    
    print("\n✅ Base de données peuplée avec succès !")

if __name__ == '__main__':
    main()
