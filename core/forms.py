from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Inscription, Province, Ville, Etablissement, Filiere, Matiere


class CustomUserCreationForm(UserCreationForm):
    """Formulaire d'inscription personnalisé"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adresse email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Nom d'utilisateur"
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mot de passe'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirmer le mot de passe'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''


class InscriptionForm(forms.ModelForm):
    """Formulaire d'inscription avec informations complémentaires"""
    class Meta:
        model = Inscription
        fields = ['telephone', 'date_naissance', 'lieu_naissance', 
                  'nationalite', 'niveau_etude', 'etablissement_origine']
        widgets = {
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de téléphone'
            }),
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'lieu_naissance': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lieu de naissance'
            }),
            'nationalite': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nationalité'
            }),
            'niveau_etude': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Niveau d\'étude actuel'
            }),
            'etablissement_origine': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Établissement d\'origine'
            }),
        }


class LoginForm(forms.Form):
    """Formulaire de connexion personnalisé"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur ou email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class ProvinceForm(forms.ModelForm):
    """Formulaire pour modifier une province"""
    class Meta:
        model = Province
        fields = ['nom_province', 'code_province', 'description']
        widgets = {
            'nom_province': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la province'
            }),
            'code_province': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code de la province'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de la province'
            }),
        }


class VilleForm(forms.ModelForm):
    """Formulaire pour modifier une ville"""
    class Meta:
        model = Ville
        fields = ['nom_ville', 'code_postal', 'province', 'description']
        widgets = {
            'nom_ville': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la ville'
            }),
            'code_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code postal'
            }),
            'province': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de la ville'
            }),
        }


class EtablissementForm(forms.ModelForm):
    """Formulaire pour modifier un établissement"""
    class Meta:
        model = Etablissement
        fields = ['nom_etab', 'type_etab', 'ville', 'adresse', 'telephone', 
                  'email', 'site_web', 'description']
        widgets = {
            'nom_etab': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'établissement'
            }),
            'type_etab': forms.Select(attrs={
                'class': 'form-control'
            }),
            'ville': forms.Select(attrs={
                'class': 'form-control'
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Adresse'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Téléphone'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'site_web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Site web'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description'
            }),
        }


class FiliereForm(forms.ModelForm):
    """Formulaire pour modifier une filière"""
    class Meta:
        model = Filiere
        fields = ['nom_filiere', 'code_filiere', 'description']
        widgets = {
            'nom_filiere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la filière'
            }),
            'code_filiere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code de la filière'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de la filière'
            }),
        }


class MatiereForm(forms.ModelForm):
    """Formulaire pour modifier une matière"""
    class Meta:
        model = Matiere
        fields = ['nom_matiere', 'code_matiere', 'description', 'niveau', 'volume_horaire']
        widgets = {
            'nom_matiere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la matière'
            }),
            'code_matiere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code de la matière'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de la matière'
            }),
            'niveau': forms.Select(attrs={
                'class': 'form-control'
            }),
            'volume_horaire': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Volume horaire'
            }),
        }
