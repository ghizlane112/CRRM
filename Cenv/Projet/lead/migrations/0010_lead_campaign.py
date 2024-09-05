# Generated by Django 4.2 on 2024-09-04 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
        ('lead', '0009_remove_lead_campaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='campaigns.companypublicitaire'),
        ),
    ]
