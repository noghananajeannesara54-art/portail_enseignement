#!/usr/bin/env python
"""
Script pour ajouter plus d'établissements dans la base de données
"""

import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portail_enseignement.settings')
django.setup()

from core.models import Etablissement, Ville

def add_more_etablissements():
    """Ajouter plus d'établissements dans la base de données"""
    
    print("🏫 Ajout d'établissements supplémentaires...")
    
    # Récupérer toutes les villes
    villes = Ville.objects.all()
    villes_dict = {ville.nom_ville: ville for ville in villes}
    
    # Données des établissements supplémentaires
    etablissements_data = [
        # Libreville
        ('Université des Sciences de la Santé', villes_dict['Libreville'], 'public', 'Avenue de la Santé, Libreville', '+241 01 73 45 72', 'uss@enseignement-sup.ga'),
        ('Institut Supérieur de Commerce', villes_dict['Libreville'], 'public', 'Boulevard Triomphal, Libreville', '+241 01 73 45 73', 'isc@enseignement-sup.ga'),
        ('École Nationale d\'Administration', villes_dict['Libreville'], 'public', 'Place de l\'Administration, Libreville', '+241 01 73 45 74', 'ena@enseignement-sup.ga'),
        
        # Franceville
        ('Institut de Recherche Scientifique', villes_dict['Franceville'], 'public', 'Centre de Recherche, Franceville', '+241 01 73 45 75', 'irs@enseignement-sup.ga'),
        
        # Port-Gentil
        ('École Supérieure de Pétrole', villes_dict['Port-Gentil'], 'public', 'Zone Industrielle, Port-Gentil', '+241 01 73 45 76', 'esp@enseignement-sup.ga'),
        ('Institut des Techniques Marines', villes_dict['Port-Gentil'], 'public', 'Port de Pêche, Port-Gentil', '+241 01 73 45 77', 'itm@enseignement-sup.ga'),
        
        # Oyem
        ('Université du Woleu-Ntem', villes_dict['Oyem'], 'public', 'Route Nationale 2, Oyem', '+241 01 73 45 78', 'uwn@enseignement-sup.ga'),
        
        # Lambaréné
        ('Institut de Recherche Médicale', villes_dict['Lambaréné'], 'public', 'Centre Hospitalier, Lambaréné', '+241 01 73 45 79', 'irm@enseignement-sup.ga'),
        
        # Mouila
        ('École Supérieure d\'Agriculture', villes_dict['Mbigou'], 'public', 'Station Agricole, Mbigou', '+241 01 73 45 80', 'esa@enseignement-sup.ga'),
        
        # Tchibanga
        ('Institut de Développement Rural', villes_dict['Tchibanga'], 'public', 'Centre de Développement, Tchibanga', '+241 01 73 45 81', 'idr@enseignement-sup.ga'),
        
        # Makokou
        ('École de Formation Forestière', villes_dict['Makokou'], 'public', 'Centre Forestier, Makokou', '+241 01 73 45 82', 'eff@enseignement-sup.ga'),
        
        # Koulamoutou
        ('Institut des Mines et Géologie', villes_dict['Koulamoutou'], 'public', 'Zone Minière, Koulamoutou', '+241 01 73 45 83', 'img@enseignement-sup.ga'),
        
        # Bitam
        ('École Normale Supérieure du Nord', villes_dict['Bitam'], 'public', 'Quartier Administratif, Bitam', '+241 01 73 45 84', 'ensn@enseignement-sup.ga'),
        
        # Lastourville
        ('Institut de Recherche Forestière', villes_dict['Lastourville'], 'public', 'Station de Recherche, Lastourville', '+241 01 73 45 85', 'irf@enseignement-sup.ga'),
        
        # Fougamou
        ('École de Développement Local', villes_dict['Fougamou'], 'public', 'Centre de Développement, Fougamou', '+241 01 73 45 86', 'edl@enseignement-sup.ga'),
        
        # Ndjolé
        ('Institut de Recherche Hydrologique', villes_dict['Ndjolé'], 'public', 'Centre Hydrologique, Ndjolé', '+241 01 73 45 87', 'irh@enseignement-sup.ga'),
        
        # Omboué
        ('École de Techniques Pétrolières', villes_dict['Omboué'], 'public', 'Zone Pétrolière, Omboué', '+241 01 73 45 88', 'etp@enseignement-sup.ga'),
        
        # Mbigou
        ('Institut de Recherche Minière', villes_dict['Mbigou'], 'public', 'Zone Minière, Mbigou', '+241 01 73 45 89', 'irm@enseignement-sup.ga'),
        
        # Moukalaba-Doudou
        ('École de Recherche Environnementale', villes_dict['Moukalaba-Doudou'], 'public', 'Centre de Recherche, Moukalaba-Doudou', '+241 01 73 45 90', 'ere@enseignement-sup.ga'),
        
        # Ntoum (déjà un établissement, mais on en ajoute un autre)
        ('Institut de Technologie Avancée', villes_dict['Ntoum'], 'public', 'Parc Technologique, Ntoum', '+241 01 73 45 91', 'ita@enseignement-sup.ga'),
        
        # Owendo
        ('École de Logistique et Transport', villes_dict['Owendo'], 'public', 'Zone Portuaire, Owendo', '+241 01 73 45 92', 'elt@enseignement-sup.ga'),
    ]
    
    created_count = 0
    existing_count = 0
    
    for nom, ville, type_etab, adresse, telephone, email in etablissements_data:
        etablissement, created = Etablissement.objects.get_or_create(
            nom_etab=nom,
            defaults={
                'ville': ville,
                'type_etab': type_etab,
                'adresse': adresse,
                'telephone': telephone,
                'email': email,
                'description': f'Établissement public d\'enseignement supérieur situé à {ville.nom_ville}.'
            }
        )
        
        if created:
            created_count += 1
            print(f"✅ Créé: {nom} ({ville.nom_ville})")
        else:
            existing_count += 1
            print(f"⏭️ Existant: {nom} ({ville.nom_ville})")
    
    print(f"\n📊 Résumé:")
    print(f"   Établissements créés: {created_count}")
    print(f"   Établissements existants: {existing_count}")
    print(f"   Total dans la base: {Etablissement.objects.count()}")
    
    # Vérification par ville
    print(f"\n🏙️ Distribution par ville:")
    for ville in villes:
        count = Etablissement.objects.filter(ville=ville).count()
        if count > 0:
            print(f"   {ville.nom_ville}: {count} établissement(s)")

if __name__ == '__main__':
    add_more_etablissements()
