# Portail du Ministère de l'Enseignement Supérieur du Gabon

Une application web complète pour la gestion des établissements d'enseignement supérieur, filières, matières et supports de cours au Gabon.

## 🎯 Objectifs du Projet

Ce portail permet de :
- **Naviguer** par province → ville → établissement → filière → niveau → matière
- **Consulter** les supports de cours et les enseignants
- **Gérer** administrativement toutes les données (CRUD complet)
- **Télécharger** les supports de cours pour les étudiants authentifiés

## 🏗️ Architecture Technique

### Backend
- **Framework**: Django 4.2.7 (Python)
- **Base de données**: SQLite (développement) / MySQL (production)
- **Admin**: Interface Django admin automatique

### Frontend
- **Template Engine**: Django Templates
- **CSS Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Charts**: Chart.js

## 📊 Structure des Données

### Hiérarchie Principale
```
Provinces (9) → Villes → Établissements → Filières → Niveaux (L1-L3, M1-M2) → Matières → Supports de cours
```

### Modèles Principaux
- **Province**: 9 provinces du Gabon
- **Ville**: Villes par province
- **Établissement**: Public/Privé par ville
- **Filière**: Programmes d'étude par établissement
- **Niveau**: L1, L2, L3, M1, M2 par filière
- **Matière**: Cours par niveau
- **Enseignant**: Professeurs et leurs spécialités
- **SupportCours**: Documents pédagogiques par matière

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.8+
- pip

### Installation
```bash
# Cloner le projet
git clone <repository-url>
cd portail_enseignement

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration et Initialisation
```bash
# Appliquer les migrations
python manage.py migrate

# Initialiser les données de démonstration
python manage.py init_data

# Créer un superutilisateur (optionnel)
python manage.py createsuperuser
```

### Démarrage
```bash
# Démarrer le serveur de développement
python manage.py runserver
```

L'application sera accessible à : http://127.0.0.1:8000

## 👤 Comptes par Défaut

Après l'initialisation avec `init_data` :

### Administrateur
- **Username**: admin
- **Password**: admin123
- **Accès**: Administration complète + Interface publique

### Enseignant (Exemple)
- **Username**: professeur1
- **Password**: prof123
- **Accès**: Interface publique + Téléchargement des supports

## 🌐 Fonctionnalités

### Interface Publique
- **Page d'accueil** avec informations du ministère et statistiques
- **Navigation par provinces** avec menu latéral
- **Consultation hiérarchique** jusqu'aux matières
- **Affichage des supports** de cours et enseignants

### Interface Administration
- **Admin Django** : `/admin/`
- **CRUD complet** sur toutes les entités
- **Gestion des utilisateurs** et rôles
- **Upload de supports** de cours

### Authentification
- **Système de login/logout**
- **Rôles** : Admin, Enseignant, Étudiant
- **Permissions** adaptées selon le rôle

## 📱 Navigation dans l'Application

1. **Page d'accueil** : Vue d'ensemble et statistiques
2. **Choix de la province** : Menu latéral ou cartes
3. **Sélection de la ville** : Liste des villes de la province
4. **Choix de l'établissement** : Établissements publics/privés
5. **Sélection de la filière** : Programmes disponibles
6. **Choix du niveau** : L1, L2, L3, M1, M2
7. **Consultation des matières** : Liste des cours
8. **Accès aux supports** : Téléchargement des documents

## 🔧 Personnalisation

### Ajouter de nouvelles provinces
Utiliser l'interface admin ou modifier le script `init_data.py`

### Adapter les styles
- Modifier `static/css/` pour les styles personnalisés
- Les templates utilisent Bootstrap 5

### Configuration MySQL
Décommenter la section MySQL dans `settings.py` et configurer :
- DB_NAME
- DB_USER  
- DB_PASSWORD
- DB_HOST
- DB_PORT

## 📈 Statistiques Incluses

- Nombre de provinces, villes, établissements, filières
- Répartition par type d'établissement
- Volume horaire par matière
- Nombre de supports de cours

## 🎨 Design et UX

- **Design moderne** avec Bootstrap 5
- **Interface responsive** pour mobile/desktop
- **Navigation intuitive** avec breadcrumbs
- **Charts interactifs** pour les statistiques
- **Animations subtiles** et transitions fluides

## 🔒 Sécurité

- **Hashage des mots de passe** avec Django
- **Protection CSRF** sur les formulaires
- **Validation des entrées** utilisateur
- **Permissions par rôle**

## 📝 Documentation Technique

### MCD/MLD
Le fichier `MCD_MLD.md` contient :
- Modèle Conceptuel de Données
- Modèle Logique de Données  
- Scripts SQL de création

### API Endpoints
- `/api/provinces/` : Liste des provinces
- `/api/villes/<province_id>/` : Villes d'une province
- `/api/etablissements/<ville_id>/` : Établissements d'une ville

## 🤝 Contribution

1. Forker le projet
2. Créer une branche feature
3. Commiter les changements
4. Pusher vers la branche
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence [MIT](LICENSE).

## 📞 Contact

Pour toute question ou suggestion :
- Ministère de l'Enseignement Supérieur du Gabon
- Email : contact@gabon.edu

---

**Développé avec ❤️ pour l'éducation au Gabon**
