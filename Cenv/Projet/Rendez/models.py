from django.db import models

# Create your models here.
from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    heur = models.TimeField()  # Champ pour l'heure de l'événement
    lieu=models.CharField(max_length=50,null=True,blank=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Champ pour associer un événement à un utilisateur
    deleted = models.BooleanField(default=False)  # Champ pour savoir si l'événement a été supprimé
    deleted_at = models.DateTimeField(null=True, blank=True)  # Champ pour la date de suppression


    def __str__(self):
        return self.title


class History(models.Model):
    ACTION_CHOICES = [
        ('add', 'Add'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    reason = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Enregistrement de l'utilisateur
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.title} -  le {self.timestamp}"





class DeletedEvent(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    heur = models.TimeField()
    description = models.TextField()
    deletion_date = models.DateTimeField(auto_now_add=True)
    deletion_reason = models.TextField()
