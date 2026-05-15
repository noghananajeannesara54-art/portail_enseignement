from django.db import models
from django.contrib.auth.models import User


class Province(models.Model):
    """Modèle pour les provinces du Gabon"""
    nom_province = models.CharField(max_length=100, verbose_name="Nom de la province")
    code_province = models.CharField(max_length=10, verbose_name="Code de la province")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"
        ordering = ['nom_province']
    
    def __str__(self):
        return self.nom_province


class Ville(models.Model):
    """Modèle pour les villes du Gabon"""
    nom_ville = models.CharField(max_length=100, verbose_name="Nom de la ville")
    code_postal = models.CharField(max_length=20, blank=True, null=True, verbose_name="Code postal")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='villes', verbose_name="Province")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Ville"
        verbose_name_plural = "Villes"
        ordering = ['nom_ville']
    
    def __str__(self):
        return f"{self.nom_ville} ({self.province.nom_province})"


class Filiere(models.Model):
    """Modèle pour les filières d'études"""
    nom_filiere = models.CharField(max_length=100, verbose_name="Nom de la filière")
    code_filiere = models.CharField(max_length=10, verbose_name="Code de la filière")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ['nom_filiere']
    
    def __str__(self):
        return self.nom_filiere


class Niveau(models.Model):
    """Modèle pour les niveaux d'études"""
    nom_niveau = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nom du niveau")
    code_niveau = models.CharField(max_length=10, blank=True, null=True, verbose_name="Code du niveau")
    
    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ['nom_niveau']
    
    def __str__(self):
        return self.nom_niveau or f"Niveau {self.id}"


class Matiere(models.Model):
    """Modèle pour les matières"""
    nom_matiere = models.CharField(max_length=100, verbose_name="Nom de la matière")
    code_matiere = models.CharField(max_length=10, verbose_name="Code de la matière")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='matieres', 
                            verbose_name="Niveau")
    volume_horaire = models.PositiveIntegerField(verbose_name="Volume horaire")
    
    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['nom_matiere']
    
    def __str__(self):
        return self.nom_matiere


class Etablissement(models.Model):
    """Modèle pour les établissements d'enseignement supérieur"""
    TYPE_ETABLISSEMENT_CHOICES = [
        ('universite', 'Université'),
        ('ecole_sup', 'École Supérieure'),
        ('institut', 'Institut'),
        ('centre', 'Centre de Recherche'),
    ]
    
    nom_etab = models.CharField(max_length=200, verbose_name="Nom de l'établissement")
    type_etab = models.CharField(max_length=20, choices=TYPE_ETABLISSEMENT_CHOICES, 
                               verbose_name="Type d'établissement")
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, related_name='etablissements', 
                           verbose_name="Ville")
    adresse = models.TextField(verbose_name="Adresse")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    site_web = models.URLField(blank=True, null=True, verbose_name="Site web")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    filieres = models.ManyToManyField(Filiere, related_name='etablissements', 
                                   verbose_name="Filières", blank=True)
    matieres = models.ManyToManyField(Matiere, related_name='etablissements', 
                                   verbose_name="Matières", blank=True)
    niveaux = models.ManyToManyField(Niveau, related_name='etablissements', 
                                   verbose_name="Niveaux", blank=True)
    
    class Meta:
        verbose_name = "Établissement"
        verbose_name_plural = "Établissements"
        ordering = ['nom_etab']
    
    def __str__(self):
        return self.nom_etab


class Inscription(models.Model):
    """Modèle pour les inscriptions"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=100, verbose_name="Lieu de naissance")
    nationalite = models.CharField(max_length=50, verbose_name="Nationalité")
    niveau_etude = models.CharField(max_length=100, verbose_name="Niveau d'étude actuel")
    etablissement_origine = models.CharField(max_length=200, verbose_name="Établissement d'origine")
    
    class Meta:
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"
    
    def __str__(self):
        return f"Inscription de {self.user.username}"


class Enseignant(models.Model):
    """Modèle pour les enseignants"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    specialite = models.CharField(max_length=100, blank=True, null=True, verbose_name="Spécialité")
    grade = models.CharField(max_length=50, blank=True, null=True, verbose_name="Grade")
    etablissement = models.ForeignKey(Etablissement, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='enseignants', verbose_name="Établissement")
    matieres = models.ManyToManyField(Matiere, related_name='enseignants', verbose_name="Matières", blank=True)
    
    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialite}"


class SupportCours(models.Model):
    """Modèle pour les supports de cours"""
    titre = models.CharField(max_length=200, blank=True, null=True, verbose_name="Titre")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='supports', 
                               verbose_name="Matière")
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, 
                                  related_name='supports', verbose_name="Enseignant")
    fichier_support = models.FileField(upload_to='supports/', verbose_name="Fichier de support")
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    
    class Meta:
        verbose_name = "Support de cours"
        verbose_name_plural = "Supports de cours"
        ordering = ['-date_ajout']
    
    def __str__(self):
        return self.titre or f"Support {self.id}"
