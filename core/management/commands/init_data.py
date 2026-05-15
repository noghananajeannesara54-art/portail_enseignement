from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Province, Ville, Etablissement, Filiere, Niveau, Matiere, Enseignant, SupportCours


class Command(BaseCommand):
    help = 'Initialize the database with sample data for the Gabon education portal'

    def handle(self, *args, **options):
        self.stdout.write('Initializing database with sample data...')
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@gabon.edu', 'admin123')
            self.stdout.write('Created admin user: admin/admin123')
        
        # Create provinces
        provinces_data = [
            ('Estuaire', 'EST', 'Province de l\'Estuaire, capitale Libreville'),
            ('Haut-Ogooué', 'HO', 'Province du Haut-Ogooué, capitale Franceville'),
            ('Moyen-Ogooué', 'MO', 'Province du Moyen-Ogooué, capitale Lambaréné'),
            ('Ngounié', 'NGN', 'Province de la Ngounié, capitale Mouila'),
            ('Nyanga', 'NYA', 'Province de la Nyanga, capitale Tchibanga'),
            ('Ogooué-Ivindo', 'OI', 'Province de l\'Ogooué-Ivindo, capitale Makokou'),
            ('Ogooué-Lolo', 'OL', 'Province de l\'Ogooué-Lolo, capitale Koulamoutou'),
            ('Ogooué-Maritime', 'OM', 'Province de l\'Ogooué-Maritime, capitale Port-Gentil'),
            ('Woleu-Ntem', 'WN', 'Province du Woleu-Ntem, capitale Oyem'),
        ]
        
        created_provinces = []
        for name, code, desc in provinces_data:
            province, created = Province.objects.get_or_create(
                nom_province=name,
                defaults={'code_province': code, 'description': desc}
            )
            created_provinces.append(province)
            if created:
                self.stdout.write(f'Created province: {name}')
        
        # Create cities for Estuaire (example)
        estuaire = Province.objects.get(nom_province='Estuaire')
        villes_estuaire = [
            ('Libreville', 'Capitale du Gabon et chef-lieu de l\'Estuaire'),
            ('Owendo', 'Port maritime principal'),
            ('Ntoum', 'Ville historique de l\'Estuaire'),
        ]
        
        for ville_name, desc in villes_estuaire:
            ville, created = Ville.objects.get_or_create(
                nom_ville=ville_name,
                province=estuaire,
                defaults={'description': desc}
            )
            if created:
                self.stdout.write(f'Created city: {ville_name}')
        
        # Create establishments in Libreville
        libreville = Ville.objects.get(nom_ville='Libreville')
        etablissements_libreville = [
            ('Université Omar Bongo', 'public', 'Avenue Omar Bongo, Libreville', 'contact@uob.ga'),
            ('Institut National des Postes et Télécommunications', 'public', 'Avenue des Forces Armées, Libreville', 'info@inptic.ga'),
            ('École Normale Supérieure', 'public', 'Libreville', 'ens@education.ga'),
        ]
        
        for etab_name, etab_type, adresse, email in etablissements_libreville:
            etab, created = Etablissement.objects.get_or_create(
                nom_etab=etab_name,
                ville=libreville,
                defaults={
                    'type_etab': etab_type,
                    'adresse': adresse,
                    'email': email,
                    'description': f'Établissement public d\'enseignement supérieur situé à {libreville.nom_ville}'
                }
            )
            if created:
                self.stdout.write(f'Created establishment: {etab_name}')
        
        # Create filieres for INPTIC
        inptic = Etablissement.objects.get(nom_etab='Institut National des Postes et Télécommunications')
        filieres_inptic = [
            ('MTIC', 'Mathématiques et Technologies de l\'Information et de la Communication', 'MTIC'),
            ('RT', 'Réseaux et Télécommunications', 'RT'),
            ('GI', 'Génie Informatique', 'GI'),
        ]
        
        for filiere_name, desc, code in filieres_inptic:
            filiere, created = Filiere.objects.get_or_create(
                nom_filiere=filiere_name,
                etablissement=inptic,
                defaults={'code_filiere': code, 'description': desc}
            )
            if created:
                self.stdout.write(f'Created program: {filiere_name}')
        
        # Create levels for MTIC
        mtic = Filiere.objects.get(nom_filiere='MTIC')
        niveaux_mtic = ['L1', 'L2', 'L3']
        
        for niveau_code in niveaux_mtic:
            niveau, created = Niveau.objects.get_or_create(
                libelle_niveau=niveau_code,
                filiere=mtic,
                defaults={'description': f'{niveau_code} en {mtic.nom_filiere}'}
            )
            if created:
                self.stdout.write(f'Created level: {niveau_code} {mtic.nom_filiere}')
        
        # Create subjects for L1 MTIC
        l1_mtic = Niveau.objects.get(libelle_niveau='L1', filiere=mtic)
        matieres_l1 = [
            ('Algorithmique', 'ALGO', 'Introduction aux algorithmes', 60),
            ('Programmation', 'PROG', 'Programmation structurée', 75),
            ('Mathématiques', 'MATH', 'Mathématiques fondamentales', 90),
            ('Base de Données', 'BDD', 'Introduction aux bases de données', 45),
            ('Réseaux', 'RES', 'Concepts de base des réseaux', 60),
        ]
        
        for matiere_name, code, desc, volume in matieres_l1:
            matiere, created = Matiere.objects.get_or_create(
                nom_matiere=matiere_name,
                niveau=l1_mtic,
                defaults={
                    'code_matiere': code,
                    'description': desc,
                    'volume_horaire': volume
                }
            )
            if created:
                self.stdout.write(f'Created subject: {matiere_name}')
        
        # Create a sample teacher
        teacher_user, created = User.objects.get_or_create(
            username='professeur1',
            defaults={
                'email': 'prof1@gabon.edu',
                'first_name': 'Jean',
                'last_name': 'Dupont'
            }
        )
        if created:
            teacher_user.set_password('prof123')
            teacher_user.save()
        
        enseignant, created = Enseignant.objects.get_or_create(
            user=teacher_user,
            defaults={
                'nom_enseignant': 'Dupont',
                'prenom_enseignant': 'Jean',
                'email': 'prof1@gabon.edu',
                'specialite': 'Informatique',
                'grade': 'Professeur'
            }
        )
        if created:
            self.stdout.write('Created teacher: Jean Dupont')
        
        # Create a sample course support
        prog_matiere = Matiere.objects.get(nom_matiere='Programmation', niveau=l1_mtic)
        support, created = SupportCours.objects.get_or_create(
            titre_support='Cours de Programmation L1',
            matiere=prog_matiere,
            niveau=l1_mtic,
            enseignant=enseignant,
            defaults={
                'description': 'Support de cours complet pour le module de programmation en L1 MTIC',
                'type_fichier': 'PDF',
                'taille_fichier': 2048576  # 2MB
            }
        )
        if created:
            self.stdout.write('Created course support: Programmation L1')
        
        self.stdout.write(self.style.SUCCESS('Database initialization completed successfully!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Teacher: professeur1 / prof123')
