from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    
    # Pages statiques
    path('actualites/', views.actualites, name='actualites'),
    path('missions/', views.missions, name='missions'),
    path('contact/', views.contact, name='contact'),
    
    # Provinces
    path('provinces/', views.provinces_list, name='provinces_list'),
    
    # Détails
    path('province/<int:pk>/', views.province_detail, name='province_detail'),
    path('ville/<int:pk>/', views.ville_detail, name='ville_detail'),
    path('etablissement/<int:pk>/', views.etablissement_detail, name='etablissement_detail'),
    path('filiere/<int:pk>/', views.filiere_detail, name='filiere_detail'),
    path('matiere/<int:pk>/', views.matiere_detail, name='matiere_detail'),
    
    # Actions admin
    path('province/<int:pk>/edit/', views.edit_province, name='edit_province'),
    
    # API
    path('api/villes/<int:province_id>/', views.api_villes_by_province, name='api_villes_by_province'),
    path('api/etablissements/<int:ville_id>/', views.api_etablissements_by_ville, name='api_etablissements_by_ville'),
    
    # Téléchargement
    path('download/support/<int:support_id>/', views.download_support, name='download_support'),
]
