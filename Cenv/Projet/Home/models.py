from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# rendez/models.py
from django.db import models
from Rendez.models import Event 

class Appointment(models.Model):
    nom = models.CharField(max_length=100)
    prenom=models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    appointment_date = models.DateTimeField()
    lieu=models.CharField(max_length=50,null=True,blank=True)
    message = models.TextField(blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)  # Relation à Event

    
    def __str__(self):
        return f"{self.name} - {self.appointment_date}"
