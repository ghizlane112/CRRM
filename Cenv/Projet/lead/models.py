from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()



# Create your models here.
class Lead(models.Model):
    STATUTS=[
      ('Nouveau','Nouveau'),
      ('Contacte','Contacte'),
      ('Qualifie','Qualifie'),
      ('Converti','Converti'),
      ('Perdu','Perdu')

    ]
    id=models.AutoField(primary_key=True)
    nom=models.CharField(max_length=20)
    prenom=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    telephone=models.CharField(max_length=10)
    source=models.CharField(max_length=100)
    statut=models.CharField(max_length=50,choices=STATUTS,default='Nouveau')
    note=models.TextField(blank=True,null=True)
    date_creation=models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    




class Interaction(models.Model):
    INTERACTION_TYPE_CHOICES = [
        ('appel', 'Appel'),
        ('email', 'Email'),
        ('sms','SMS'),
        ('autre', 'Autre'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='interactions')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    type_interaction = models.CharField(max_length=10, choices=INTERACTION_TYPE_CHOICES)
    date_interaction = models.DateTimeField()
    note = models.TextField()
    
    def _str_(self):
        return f"{self.get_type_interaction_display()} avec {self.lead.nom} le {self.date_interaction}"

    class Meta:
        ordering = ['-date_interaction']





class Note(models.Model):
    lead = models.ForeignKey(Lead, related_name='notes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Note for {self.lead.nom} {self.lead.prenom} by {self.user.username}"




class LeadHistory(models.Model):
    ACTION_CHOICES = (
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
    )
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.get_action_display()} by {self.user} on {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']  # Pour trier par date décroissante par défaut




        