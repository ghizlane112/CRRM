from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone 

class Users(AbstractUser):
    nom = models.CharField(max_length=15)
    prenom = models.CharField(max_length=15)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
   # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    last_activity = models.DateTimeField(default=timezone.now)  # Ajouté pour suivre la dernière activité

    # Ajoutez d'autres champs selon vos besoins

    # Redéfinir les relations pour éviter les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='users_set',
        blank=True
    )
