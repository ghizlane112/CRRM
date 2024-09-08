# Generated by Django 4.2 on 2024-09-08 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rendez', '0007_deletedevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
