# Generated by Django 5.1 on 2024-08-31 00:30

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=20)),
                ('prenom', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telephone', models.CharField(max_length=10)),
                ('source', models.CharField(max_length=100)),
                ('statut', models.CharField(choices=[('Nouveau', 'Nouveau'), ('Contacte', 'Contacte'), ('Qualifie', 'Qualifie'), ('Converti', 'Converti'), ('Perdu', 'Perdu')], default='Nouveau', max_length=50)),
                ('note', models.TextField(blank=True, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('responsable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_interaction', models.CharField(choices=[('appel', 'Appel'), ('email', 'Email'), ('sms', 'SMS'), ('autre', 'Autre')], max_length=10)),
                ('date_interaction', models.DateTimeField()),
                ('note', models.TextField()),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interactions', to='lead.lead')),
            ],
            options={
                'ordering': ['-date_interaction'],
            },
        ),
        migrations.CreateModel(
            name='LeadHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('created', 'Created'), ('updated', 'Updated'), ('deleted', 'Deleted')], max_length=10)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('details', models.TextField(blank=True, null=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lead.lead')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='lead.lead')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
