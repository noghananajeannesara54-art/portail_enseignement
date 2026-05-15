# 🚀 Guide d'Installation et Configuration

## 📋 Prérequis

1. **Python 3.8+** installé
2. **MySQL Server** installé et en cours d'exécution
3. **Navigateur web** moderne

## 🛠️ Étapes d'Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd portail_enseignement
```

### 2. Créer l'environnement virtuel
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données MySQL

#### Option A: Avec MySQL Server
```sql
-- Se connecter à MySQL
mysql -u root -p

-- Créer la base de données
CREATE DATABASE IF NOT EXISTS portail_enseignement CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Créer l'utilisateur
CREATE USER IF NOT EXISTS 'portail_user'@'localhost' IDENTIFIED BY 'portail123';

-- Donner les privilèges
GRANT ALL PRIVILEGES ON portail_enseignement.* TO 'portail_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Option B: Avec XAMPP/WAMP
```sql
-- Via phpMyAdmin ou interface MySQL
CREATE DATABASE IF NOT EXISTS portail_enseignement CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'portail_user'@'localhost' IDENTIFIED BY 'portail123';
GRANT ALL PRIVILEGES ON portail_enseignement.* TO 'portail_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configurer Django
Mettre à jour `portail_enseignement/portail_enseignement/settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portail_enseignement',
        'USER': 'portail_user',
        'PASSWORD': 'portail123',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### 6. Créer les migrations
```bash
python manage.py makemigrations
```

### 7. Appliquer les migrations
```bash
python manage.py migrate
```

### 8. Initialiser les données
```bash
python manage.py init_data
```

### 9. Créer le superutilisateur (optionnel)
```bash
python manage.py createsuperuser
```

### 10. Lancer le serveur
```bash
python manage.py runserver
```

## 🌐 Accès à l'Application

- **URL principale**: http://127.0.0.1:8000
- **Admin Django**: http://127.0.0.1:8000/admin
- **Inscription**: http://127.0.0.1:8000/register
- **Connexion**: http://127.0.0.1:8000/login

## 👤 Comptes par Défaut

### Administrateur
- **Username**: admin
- **Password**: admin123
- **Accès**: Administration complète + Interface publique

### Enseignant (Exemple)
- **Username**: professeur1
- **Password**: prof123
- **Accès**: Interface publique + Téléchargement des supports

### Étudiant
- **Inscription**: Via formulaire d'inscription
- **Accès**: Interface publique + Téléchargement des supports (après inscription)

## 🎯 Fonctionnalités Implémentées

### ✅ Interface Utilisateur
- **Page d'accueil** avec présentation du ministère et du ministre
- **Navigation hiérarchique**: Province → Ville → Établissement → Filière → Niveau → Matière
- **Inscription/Connexion**: Formulaire complet avec validation
- **Téléchargement**: Réservé aux utilisateurs enregistrés
- **Profil utilisateur**: Informations personnelles et historique

### ✅ Interface Administrateur
- **Édition directe**: Modifier provinces, villes, établissements, filières, matières depuis le site
- **Admin Django**: Interface complète pour toutes les entités
- **Gestion des utilisateurs**: Voir et gérer les inscriptions
- **Upload de supports**: Ajouter des documents pédagogiques

### ✅ Base de Données
- **9 provinces** du Gabon avec villes
- **Établissements** publics et privés par ville
- **Filières** et niveaux (L1, L2, L3, M1, M2)
- **Matières** avec enseignants et supports de cours
- **Inscriptions** avec informations complémentaires

## 🔧 Personnalisation

### Modifier les couleurs et styles
- **Fichier**: `templates/core/home.html`
- **CSS**: Classes Bootstrap personnalisées dans `<style>` blocks
- **Images**: Remplacer les placeholders par les vraies photos

### Ajouter de nouvelles provinces
- **Via admin**: http://127.0.0.1:8000/admin/core/province/
- **Via formulaire**: http://127.0.0.1:8000/edit/province/new/

### Personnaliser les messages
- **Fichier**: `portail_enseignement/settings.py`
- **Messages**: Modifier `MESSAGES` settings

## 🚨 Dépannage

### Erreurs Communes

#### ModuleNotFoundError: No module named 'mysqlclient'
```bash
pip install mysqlclient
```

#### Authentication error 'Access denied for user'
```bash
# Vérifier les identifiants MySQL dans settings.py
# Redémarrer le serveur MySQL
```

#### Table doesn't exist
```bash
python manage.py migrate
```

#### TemplateDoesNotExist
```bash
# Vérifier que les templates existent dans core/templates/
```

## 📊 Structure du Projet

```
portail_enseignement/
├── core/                          # Application principale
│   ├── models.py               # Modèles de données
│   ├── views.py                # Vues et logique
│   ├── forms.py                # Formulaires
│   ├── urls.py                 # URLs de l'application
│   ├── admin.py                # Configuration admin
│   └── templates/              # Templates HTML
│       ├── base.html           # Template de base
│       ├── home.html           # Page d'accueil
│       ├── register.html        # Inscription
│       ├── login.html          # Connexion
│       └── *.html              # Autres templates
├── portail_enseignement/         # Configuration Django
│   ├── settings.py            # Paramètres du projet
│   ├── urls.py               # URLs principales
│   └── wsgi.py               # Déploiement
├── requirements.txt              # Dépendances Python
├── manage.py                   # Script de gestion Django
└── README.md                   # Documentation du projet
```

## 🎨 Design et UX

### Technologies Utilisées
- **Backend**: Django 4.2.7 (Python)
- **Frontend**: Bootstrap 5 + Font Awesome 6
- **Base de données**: MySQL 8.0
- **Charts**: Chart.js pour les statistiques

### Responsive Design
- **Mobile-first**: Adapté pour tous les écrans
- **Navigation**: Menu latéral pour desktop, menu burger pour mobile
- **Animations**: Transitions CSS3 et JavaScript moderne

## 🔒 Sécurité

### Authentification
- **Hashage**: Django password hashing par défaut
- **Sessions**: Sécurisées avec durée configurable
- **CSRF**: Protection automatique sur tous les formulaires
- **Permissions**: Rôles définis (admin, enseignant, étudiant)

### Validation
- **Formulaires**: Validation côté client et serveur
- **Données**: Échappement automatique des entrées
- **URLs**: Protection contre les injections SQL

## 📈 Performance

### Optimisations
- **Queries**: Utilisation de `select_related` et `prefetch_related`
- **Static files**: Compression et cache
- **Database**: Indexation appropriée des champs
- **Pagination**: Pour les grandes listes de données

## 🌍 Déploiement

### Production
```bash
# Collecter les fichiers statiques
python manage.py collectstatic

# Utiliser un serveur WSGI (Gunicorn, uWSGI)
gunicorn portail_enseignement.wsgi:application
```

### Variables d'environnement
```bash
export DJANGO_SETTINGS_MODULE=portail_enseignement.settings.production
export DATABASE_URL=mysql://portail_user:portail123@localhost:3306/portail_enseignement
```

## 📞 Support

### Documentation Complète
- **MCD/MLD**: `MCD_MLD.md` avec schéma de la base
- **API**: Endpoints REST pour les données dynamiques
- **Tests**: Scripts de test pour les fonctionnalités clés

### Ressources
- **Django Docs**: https://docs.djangoproject.com/
- **Bootstrap**: https://getbootstrap.com/docs/
- **MySQL**: https://dev.mysql.com/doc/

---

## 🎉 Félicitations !

Votre portail éducatif du Gabon est maintenant prêt avec :

✅ **Interface moderne** et professionnelle  
✅ **Système d'inscription** complet  
✅ **Gestion admin** avancée  
✅ **Base de données MySQL** optimisée  
✅ **Navigation hiérarchique** intuitive  
✅ **Téléchargement sécurisé** pour les inscrits  

**Développé avec ❤️ pour l'éducation au Gabon**
