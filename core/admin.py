from django.contrib import admin
from .models import Province, Ville, Etablissement, Filiere, Niveau, Matiere, Inscription, Enseignant, SupportCours


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    """Configuration admin pour les provinces"""
    list_display = ('nom_province', 'code_province', 'description')
    list_filter = ('code_province',)
    search_fields = ('nom_province', 'code_province')
    ordering = ('nom_province',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom_province', 'code_province', 'description'),
        }),
    )


@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    """Configuration admin pour les villes"""
    list_display = ('nom_ville', 'code_postal', 'province', 'description')
    list_filter = ('province',)
    search_fields = ('nom_ville', 'code_postal', 'province__nom_province')
    ordering = ('nom_ville',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom_ville', 'code_postal', 'province'),
        }),
        ('Description', {
            'fields': ('description',),
        }),
    )


@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    """Configuration admin pour les établissements"""
    list_display = ('nom_etab', 'type_etab', 'ville', 'telephone', 'email')
    list_filter = ('type_etab', 'ville__province')
    search_fields = ('nom_etab', 'adresse', 'ville__nom_ville')
    ordering = ('nom_etab',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom_etab', 'type_etab', 'ville'),
        }),
        ('Coordonnées', {
            'fields': ('adresse', 'telephone', 'email', 'site_web'),
        }),
        ('Description', {
            'fields': ('description',),
        }),
    )


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    """Configuration admin pour les filières"""
    list_display = ('nom_filiere', 'code_filiere', 'description')
    search_fields = ('nom_filiere', 'code_filiere')
    ordering = ('nom_filiere',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom_filiere', 'code_filiere', 'description'),
        }),
    )


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    """Configuration admin pour les niveaux"""
    list_display = ('nom_niveau', 'code_niveau')
    search_fields = ('nom_niveau', 'code_niveau')
    ordering = ('nom_niveau',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom_niveau', 'code_niveau'),
        }),
    )


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    """Configuration admin pour les matières"""
    list_display = ('nom_matiere', 'code_matiere', 'niveau', 'volume_horaire')
    list_filter = ('niveau',)
    search_fields = ('nom_matiere', 'code_matiere', 'niveau__nom_niveau')
    ordering = ('nom_matiere',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom_matiere', 'code_matiere', 'niveau'),
        }),
        ('Détails', {
            'fields': ('volume_horaire', 'description'),
        }),
    )


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    """Configuration admin pour les inscriptions"""
    list_display = ('user', 'telephone', 'date_naissance', 'nationalite', 'niveau_etude')
    list_filter = ('nationalite', 'niveau_etude')
    search_fields = ('user__username', 'user__email', 'telephone')
    ordering = ('user__username',)
    
    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('user',),
        }),
        ('Informations personnelles', {
            'fields': ('telephone', 'date_naissance', 'lieu_naissance', 'nationalite'),
        }),
        ('Informations académiques', {
            'fields': ('niveau_etude', 'etablissement_origine'),
        }),
    )


@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    """Configuration admin pour les enseignants"""
    list_display = ('user', 'specialite', 'grade', 'etablissement')
    list_filter = ('grade', 'etablissement__ville__province')
    search_fields = ('user__username', 'user__get_full_name', 'specialite')
    ordering = ('user__username',)
    filter_horizontal = ('matieres',)
    
    fieldsets = (
        ('Informations utilisateur', {
            'fields': ('user',),
        }),
        ('Informations professionnelles', {
            'fields': ('specialite', 'grade', 'etablissement'),
        }),
        ('Matières enseignées', {
            'fields': ('matieres',),
        }),
    )


@admin.register(SupportCours)
class SupportCoursAdmin(admin.ModelAdmin):
    """Configuration admin pour les supports de cours"""
    list_display = ('titre', 'matiere', 'enseignant', 'date_ajout')
    list_filter = ('matiere', 'enseignant', 'date_ajout')
    search_fields = ('titre', 'description', 'matiere__nom_matiere')
    ordering = ('-date_ajout',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'description'),
        }),
        ('Association', {
            'fields': ('matiere', 'enseignant'),
        }),
        ('Fichier', {
            'fields': ('fichier_support',),
        }),
    )
