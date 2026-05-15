# Generated migration for adding ManyToMany relations to Etablissement

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='etablissement',
            name='filieres',
            field=models.ManyToManyField(blank=True, related_name='etablissements', to='core.filiere', verbose_name='Filières'),
        ),
        migrations.AddField(
            model_name='etablissement',
            name='matieres',
            field=models.ManyToManyField(blank=True, related_name='etablissements', to='core.matiere', verbose_name='Matières'),
        ),
        migrations.AddField(
            model_name='etablissement',
            name='niveaux',
            field=models.ManyToManyField(blank=True, related_name='etablissements', to='core.niveau', verbose_name='Niveaux'),
        ),
    ]
