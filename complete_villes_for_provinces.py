#!/usr/bin/env python
"""
Script pour compléter les villes manquantes afin que chaque province ait 9 villes
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portail_enseignement.settings')
django.setup()

from core.models import Province, Ville

def complete_villes_for_provinces():
    """Ajouter des villes pour que chaque province en ait 9"""
    
    print("🏙️  Complétion des villes pour chaque province...")
    
    # Noms de villes supplémentaires pour chaque province
    villes_supplementaires = {
        'Estuaire': ['Akanda', 'Ntoum', 'Cocobeach', 'Kango', 'Nkol', 'Bongolo'],
        'Haut-Ogooué': ['Lékoni', 'Lebamba', 'Bongoville', 'Mounana', 'Moanda', 'Boungou'],
        'Moyen-Ogooué': ['Mouila', 'Fougamou', 'Ndendé', 'Mbigou', 'Lébamba', 'Silon'],
        'Ngounié': ['Mouila', 'Fougamou', 'Ndendé', 'Mbigou', 'Lébamba', 'Sindara'],
        'Nyanga': ['Tchibanga', 'Mayumba', 'Moungoundou', 'Mabanda', 'Bilinga', 'Dibisso'],
        'Ogooué-Ivindo': ['Makokou', 'Mékambo', 'Booué', 'Ovan', 'Kokoro', 'Mazingo'],
        'Ogooué-Lolo': ['Koulamoutou', 'Lastoursville', 'Poubara', 'Iboundji', 'Moulengui', 'Bongolo'],
        'Ogooué-Maritime': ['Port-Gentil', 'Omboué', 'Gamba', 'Mandilou', 'Sette Cama', 'Cap Lopez'],
        'Woleu-Ntem': ['Oyem', 'Bitam', 'Mitzic', 'Mekam', 'Minvoul', 'Medouneu']
    }
    
    provinces = Province.objects.all()
    total_created = 0
    
    for province in provinces:
        print(f"\n🏛️  {province.nom_province}")
        
        # Villes existantes
        existing_villes = Ville.objects.filter(province=province)
        existing_count = existing_villes.count()
        existing_names = [v.nom_ville for v in existing_villes]
        
        print(f"   - Villes existantes: {existing_count}/9")
        
        if existing_count >= 9:
            print(f"   ✅ Déjà complet!")
            continue
        
        # Ajouter les villes manquantes
        needed = 9 - existing_count
        print(f"   - Besoin de {needed} villes supplémentaires")
        
        # Prendre les noms de villes supplémentaires
        if province.nom_province in villes_supplementaires:
            available_names = villes_supplementaires[province.nom_province]
        else:
            # Noms génériques si la province n'est pas dans la liste
            available_names = [f'Ville {i+1}' for i in range(needed)]
        
        created_for_province = 0
        for i, nom_ville in enumerate(available_names):
            if created_for_province >= needed:
                break
                
            if nom_ville not in existing_names:
                ville, created = Ville.objects.get_or_create(
                    nom_ville=nom_ville,
                    province=province
                )
                
                if created:
                    total_created += 1
                    created_for_province += 1
                    print(f"   ✅ Créée: {nom_ville}")
        
        print(f"   - Total créé pour cette province: {created_for_province}")
    
    print(f"\n📊 Total de villes créées: {total_created}")
    
    # Vérification finale
    print("\n🔍 Vérification finale:")
    for province in provinces:
        count = Ville.objects.filter(province=province).count()
        status = "✅" if count == 9 else "❌"
        print(f"   {status} {province.nom_province}: {count}/9 villes")

if __name__ == '__main__':
    print("=" * 60)
    print("🏙️  COMPLÉTION DES VILLES PAR PROVINCE")
    print("=" * 60)
    
    try:
        complete_villes_for_provinces()
        
        print("\n" + "=" * 60)
        print("✅ Opération terminée!")
        print("   Chaque province devrait maintenant avoir 9 villes")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
