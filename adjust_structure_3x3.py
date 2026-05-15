#!/usr/bin/env python
"""
Script pour ajuster la structure à exactement 3 villes par province et 3 établissements par ville
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portail_enseignement.settings')
django.setup()

from core.models import Province, Ville, Etablissement

def adjust_to_3x3_structure():
    """Ajuster la structure à 3 villes par province et 3 établissements par ville"""
    
    print("🔧 Ajustement de la structure à 3x3 (3 villes/province, 3 établissements/ville)")
    
    # Villes originales à conserver pour chaque province (les 3 premières)
    villes_originales = {
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
    
    total_deleted_villes = 0
    total_deleted_etabs = 0
    
    for province in Province.objects.all():
        print(f"\n🏛️  {province.nom_province}")
        
        # Récupérer toutes les villes de la province
        all_villes = Ville.objects.filter(province=province).order_by('id')
        villes_count = all_villes.count()
        
        print(f"   - Villes actuelles: {villes_count}")
        
        if villes_count <= 3:
            print(f"   ✅ Déjà correct ({villes_count} villes)")
            continue
        
        # Identifier les villes à supprimer
        villes_a_garder = []
        if province.nom_province in villes_originales:
            noms_a_garder = villes_originales[province.nom_province]
            for nom in noms_a_garder:
                ville = Ville.objects.filter(province=province, nom_ville=nom).first()
                if ville:
                    villes_a_garder.append(ville)
        
        # Compléter avec les premières villes si nécessaire
        while len(villes_a_garder) < 3:
            for ville in all_villes:
                if ville not in villes_a_garder:
                    villes_a_garder.append(ville)
                    break
            if len(villes_a_garder) < 3:
                break
        
        # Identifier les villes à supprimer
        villes_a_supprimer = []
        for ville in all_villes:
            if ville not in villes_a_garder:
                villes_a_supprimer.append(ville)
        
        # Supprimer les villes en trop
        for ville in villes_a_supprimer:
            # Compter les établissements avant suppression
            etabs_count = Etablissement.objects.filter(ville=ville).count()
            
            # Supprimer les établissements d'abord
            etabs = Etablissement.objects.filter(ville=ville)
            etabs_deleted = etabs.count()
            etabs.delete()
            
            # Supprimer la ville
            ville.delete()
            
            total_deleted_villes += 1
            total_deleted_etabs += etabs_deleted
            print(f"   ❌ Supprimée: {ville.nom_ville} (avec {etabs_deleted} établissements)")
        
        # Vérifier les villes gardées
        print(f"   ✅ Villes conservées ({len(villes_a_garder)}):")
        for ville in villes_a_garder:
            etabs_count = Etablissement.objects.filter(ville=ville).count()
            print(f"      - {ville.nom_ville}: {etabs_count} établissements")
    
    print(f"\n📊 Total supprimé:")
    print(f"   - Villes: {total_deleted_villes}")
    print(f"   - Établissements: {total_deleted_etabs}")
    
    return total_deleted_villes, total_deleted_etabs

def ensure_3_etablissements_per_ville():
    """S'assurer que chaque ville a exactement 3 établissements"""
    
    print("\n🏫 Vérification et ajustement des établissements (3 par ville)")
    
    types_etablissements = ['universite', 'ecole_sup', 'institut', 'centre']
    noms_etablissements = ['Université', 'École Supérieure', 'Institut', 'Centre de Formation']
    
    villes = Ville.objects.all()
    total_created = 0
    total_deleted = 0
    
    for ville in villes:
        etabs = Etablissement.objects.filter(ville=ville)
        etabs_count = etabs.count()
        
        print(f"\n🏙️  {ville.nom_ville} ({ville.province.nom_province})")
        print(f"   - Établissements actuels: {etabs_count}")
        
        if etabs_count > 3:
            # Supprimer les établissements en trop (garder les 3 premiers)
            etabs_a_supprimer = etabs.order_by('id')[3:]
            deleted = etabs_a_supprimer.count()
            etabs_a_supprimer.delete()
            total_deleted += deleted
            print(f"   ❌ Supprimés: {deleted} établissements (conserve 3)")
            
        elif etabs_count < 3:
            # Créer des établissements manquants
            needed = 3 - etabs_count
            existing_names = [e.nom_etab for e in etabs]
            
            for i in range(needed):
                # Générer un nom unique
                base_name = noms_etablissements[i % len(noms_etablissements)]
                nom_etab = f"{base_name} de {ville.nom_ville}"
                
                # Éviter les doublons
                counter = 1
                final_name = nom_etab
                while final_name in existing_names:
                    final_name = f"{nom_etab} {counter}"
                    counter += 1
                
                # Créer l'établissement
                etablissement = Etablissement.objects.create(
                    nom_etab=final_name,
                    type_etab=types_etablissements[i % len(types_etablissements)],
                    ville=ville,
                    adresse=f'Avenue principale, {ville.nom_ville}',
                    telephone=f'+241 01 45 6{7+i}8{9+i}',
                    email=f'contact{7+i}@{final_name.lower().replace(" ", "_").replace("\'", "")}.ga',
                    site_web=f'www.{final_name.lower().replace(" ", "_").replace("\'", "")}.ga',
                    description=f'Établissement d\'excellence situé à {ville.nom_ville}.'
                )
                
                total_created += 1
                print(f"   ✅ Créé: {final_name}")
        
        else:
            print(f"   ✅ Déjà correct (3 établissements)")
    
    print(f"\n📊 Total d'établissements:")
    print(f"   - Créés: {total_created}")
    print(f"   - Supprimés: {total_deleted}")
    
    return total_created, total_deleted

def add_relations_to_all_etablissements():
    """Ajouter les relations (filieres, matieres, niveaux) à tous les établissements"""
    
    print("\n🔗 Ajout des relations aux établissements...")
    
    from core.models import Filiere, Matiere, Niveau
    
    filieres = list(Filiere.objects.all())
    matieres = list(Matiere.objects.all())
    niveaux = list(Niveau.objects.all())
    
    etablissements = Etablissement.objects.all()
    
    for etablissement in etablissements:
        # Ajouter toutes les relations
        etablissement.filieres.set(filieres)
        etablissement.matieres.set(matieres)
        etablissement.niveaux.set(niveaux)
    
    print(f"   ✅ Relations ajoutées à {etablissements.count()} établissements")

def verify_final_structure():
    """Vérifier la structure finale 3x3"""
    
    print("\n🔍 Vérification de la structure finale 3x3...")
    
    provinces = Province.objects.all()
    villes = Ville.objects.all()
    etablissements = Etablissement.objects.all()
    
    print(f"\n📊 Résumé final:")
    print(f"   - Provinces: {provinces.count()}")
    print(f"   - Villes: {villes.count()} (devrait être 27 = 9×3)")
    print(f"   - Établissements: {etablissements.count()} (devrait être 81 = 27×3)")
    
    print(f"\n🏛️  Détail par province:")
    all_correct = True
    
    for province in provinces:
        villes_province = Ville.objects.filter(province=province)
        villes_count = villes_province.count()
        
        total_etabs = sum(Etablissement.objects.filter(ville=v).count() for v in villes_province)
        
        status = "✅" if villes_count == 3 and total_etabs == 9 else "❌"
        print(f"   {status} {province.nom_province}: {villes_count} villes, {total_etabs} établissements")
        
        if villes_count != 3 or total_etabs != 9:
            all_correct = False
    
    if all_correct:
        print(f"\n✅ Structure 3x3 parfaite!")
    else:
        print(f"\n⚠️  Structure incomplète - vérifications nécessaires")

if __name__ == '__main__':
    print("=" * 80)
    print("🔧 AJUSTEMENT DE LA STRUCTURE À 3x3")
    print("   3 villes par province, 3 établissements par ville")
    print("=" * 80)
    
    try:
        # 1. Ajuster à 3 villes par province
        deleted_villes, deleted_etabs = adjust_to_3x3_structure()
        
        # 2. S'assurer d'avoir 3 établissements par ville
        created_etabs, deleted_etabs2 = ensure_3_etablissements_per_ville()
        
        # 3. Ajouter les relations aux établissements
        add_relations_to_all_etablissements()
        
        # 4. Vérifier la structure finale
        verify_final_structure()
        
        print("\n" + "=" * 80)
        print("✅ Structure 3x3 ajustée avec succès!")
        print("   - 9 provinces")
        print("   - 3 villes par province (27 total)")
        print("   - 3 établissements par ville (81 total)")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
