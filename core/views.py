from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from .models import Province, Ville, Etablissement, Filiere, Niveau, Matiere, Enseignant, SupportCours, Inscription
from .forms import CustomUserCreationForm, InscriptionForm, LoginForm, ProvinceForm, VilleForm, EtablissementForm, FiliereForm, MatiereForm


def home(request):
    """Vue pour la page d'accueil"""
    provinces = Province.objects.prefetch_related('villes').all()
    
    # Statistiques
    total_etablissements = Etablissement.objects.count()
    total_filieres = Filiere.objects.count()
    total_matieres = Matiere.objects.count()
    
    context = {
        'provinces': provinces,
        'total_etablissements': total_etablissements,
        'total_filieres': total_filieres,
        'total_matieres': total_matieres,
    }
    return render(request, 'core/home.html', context)


def province_detail(request, pk):
    """Vue pour afficher les détails d'une province"""
    province = get_object_or_404(Province.objects.prefetch_related('villes__etablissements'), pk=pk)
    
    # Calculer le total des établissements pour cette province
    total_etablissements = sum(ville.etablissements.count() for ville in province.villes.all())
    
    context = {
        'province': province,
        'villes': province.villes.all(),
        'total_etablissements': total_etablissements,
    }
    return render(request, 'core/province_detail.html', context)


def ville_detail(request, pk):
    """Vue pour afficher les détails d'une ville"""
    ville = get_object_or_404(Ville.objects.prefetch_related('etablissements__filieres'), pk=pk)
    
    # Calculer le total des filières pour cette ville
    total_filieres = 0
    for etab in ville.etablissements.all():
        total_filieres += etab.filieres.count()
    
    context = {
        'ville': ville,
        'etablissements': ville.etablissements.all(),
        'total_filieres': total_filieres,
    }
    return render(request, 'core/ville_detail.html', context)


def etablissement_detail(request, pk):
    """Vue pour afficher les détails d'un établissement"""

    etablissement = get_object_or_404(
        Etablissement.objects
        .select_related('ville')
        .prefetch_related('filieres', 'niveaux'),
        pk=pk
    )

    filieres = etablissement.filieres.all()

    total_niveaux = etablissement.niveaux.count()

    context = {
        'etablissement': etablissement,
        'filieres': filieres,
        'total_niveaux': total_niveaux,
    }

    return render(request, 'core/etablissement_detail.html', context)

def filiere_detail(request, pk):
    """Vue pour afficher les détails d'une filière avec niveaux et matières"""
    filiere = get_object_or_404(Filiere, pk=pk)
    
    # Récupérer tous les niveaux disponibles
    from core.models import Niveau, Matiere, Enseignant, SupportCours
    from django.db import models
    
    niveaux = Niveau.objects.all()
    
    # Organiser les données par niveau
    niveaux_avec_matieres = []
    
    for niveau in niveaux:
        # Récupérer les matières pour ce niveau qui correspondent à la filière
        filiere_keywords = filiere.nom_filiere.lower().split()
        
        matieres_niveau = Matiere.objects.none()
        
        for keyword in filiere_keywords:
            keyword_matieres = Matiere.objects.filter(
                models.Q(nom_matiere__icontains=keyword) |
                models.Q(description__icontains=keyword),
                niveau=niveau
            )
            matieres_niveau = matieres_niveau | keyword_matieres
        
        # Organiser les matières avec leurs enseignants et supports
        matieres_avec_details = []
        for matiere in matieres_niveau.distinct():
            # Récupérer les enseignants pour cette matière
            enseignants = Enseignant.objects.filter(matieres=matiere)
            
            # Récupérer les supports de cours pour cette matière
            supports = SupportCours.objects.filter(matiere=matiere)
            
            matieres_avec_details.append({
                'matiere': matiere,
                'enseignants': enseignants,
                'supports': supports,
                'nb_enseignants': enseignants.count(),
                'nb_supports': supports.count()
            })
        
        niveaux_avec_matieres.append({
            'niveau': niveau,
            'matieres': matieres_avec_details,
            'nb_matieres': len(matieres_avec_details)
        })
    
    context = {
        'filiere': filiere,
        'niveaux': niveaux_avec_matieres,
        'total_niveaux': len(niveaux_avec_matieres),
    }
    return render(request, 'core/filiere_detail.html', context)


def matiere_detail(request, pk):
    """Vue pour afficher les détails d'une matière"""
    matiere = get_object_or_404(Matiere.objects.prefetch_related('supports'), pk=pk)
    
    context = {
        'matiere': matiere,
        'supports': matiere.supports.all(),
    }
    return render(request, 'core/matiere_detail.html', context)


def actualites(request):
    """Vue pour la page des actualités"""
    context = {}
    return render(request, 'core/actualites.html', context)


def missions(request):
    """Vue pour la page des missions"""
    context = {}
    return render(request, 'core/missions.html', context)


def contact(request):
    """Vue pour la page de contact"""
    context = {}
    return render(request, 'core/contact.html', context)


def login_view(request):
    """Vue pour la connexion"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {username}!')
            return redirect('core:home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'core/login.html')


def logout_view(request):
    """Vue pour la déconnexion"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('core:home')


@login_required
def profile(request):
    """Vue pour le profil utilisateur avec informations détaillées"""
    user = request.user
    
    # Récupérer les informations supplémentaires
    inscription = None
    enseignant = None
    
    try:
        inscription = Inscription.objects.get(user=user)
    except Inscription.DoesNotExist:
        pass
    
    try:
        enseignant = Enseignant.objects.get(user=user)
    except Enseignant.DoesNotExist:
        pass
    
    # Statistiques générales
    stats = {
        'total_provinces': Province.objects.count(),
        'total_villes': Ville.objects.count(),
        'total_etablissements': Etablissement.objects.count(),
        'total_filieres': Filiere.objects.count(),
        'total_matieres': Matiere.objects.count(),
        'total_inscriptions': Inscription.objects.count(),
        'total_enseignants': Enseignant.objects.count(),
    }
    
    context = {
        'user': user,
        'inscription': inscription,
        'enseignant': enseignant,
        'stats': stats,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    }
    return render(request, 'core/profile.html', context)


def register(request):
    """Vue pour l'inscription des utilisateurs"""
    
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        inscription_form = InscriptionForm(request.POST)

        if user_form.is_valid() and inscription_form.is_valid():
            user = user_form.save()

            inscription = inscription_form.save(commit=False)
            inscription.user = user
            inscription.save()

            messages.success(request, "Compte créé avec succès !")
            return redirect('core:login')

        else:
            # 🔴 IMPORTANT : voir les erreurs
            print(user_form.errors)
            print(inscription_form.errors)

            messages.error(request, "Veuillez corriger les erreurs du formulaire.")

    else:
        user_form = CustomUserCreationForm()
        inscription_form = InscriptionForm()

    return render(request, 'core/register.html', {
        'user_form': user_form,
        'inscription_form': inscription_form,
    })
    
@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_province(request, pk):
    """Vue pour modifier une province directement sur le site"""
    province = get_object_or_404(Province, pk=pk)
    
    if request.method == 'POST':
        form = ProvinceForm(request.POST, instance=province)
        if form.is_valid():
            form.save()
            messages.success(request, f'La province {province.nom_province} a été modifiée avec succès!')
            return redirect('core:province_detail', pk=province.pk)
    else:
        form = ProvinceForm(instance=province)
    
    context = {
        'form': form,
        'province': province,
    }
    return render(request, 'core/edit_province.html', context)


def search(request):
    """Vue pour la recherche"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Recherche dans les établissements
        etablissements = Etablissement.objects.filter(
            Q(nom_etab__icontains=query) |
            Q(description__icontains=query)
        )[:5]
        
        # Recherche dans les filières
        filieres = Filiere.objects.filter(
            Q(nom_filiere__icontains=query) |
            Q(description__icontains=query)
        )[:5]
        
        # Recherche dans les matières
        matieres = Matiere.objects.filter(
            Q(nom_matiere__icontains=query) |
            Q(description__icontains=query)
        )[:5]
        
        results = {
            'etablissements': etablissements,
            'filieres': filieres,
            'matieres': matieres,
            'query': query,
        }
    
    return render(request, 'core/search_results.html', {'results': results})


def api_villes_by_province(request, province_id):
    """API pour récupérer les villes d'une province"""
    villes = Ville.objects.filter(province_id=province_id).values('id', 'nom_ville')
    return JsonResponse(list(villes), safe=False)


def api_etablissements_by_ville(request, ville_id):
    """API pour récupérer les établissements d'une ville"""
    etablissements = Etablissement.objects.filter(ville_id=ville_id).values('id', 'nom_etab', 'type_etab')
    return JsonResponse(list(etablissements), safe=False)


def provinces_list(request):
    """Vue pour lister toutes les provinces"""
    provinces = Province.objects.all().order_by('nom_province')
    
    context = {
        'provinces': provinces,
        'title': 'Provinces du Gabon',
    }
    return render(request, 'core/provinces_list.html', context)


@login_required
def download_support(request, support_id):
    """Vue pour télécharger un support de cours"""
    support = get_object_or_404(SupportCours, id=support_id)
    
    # Log du téléchargement (optionnel)
    # DownloadLog.objects.create(user=request.user, support=support)
    
    response = redirect(support.fichier_support.url)
    return response
