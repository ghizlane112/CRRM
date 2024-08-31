from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
# Create your models here.


class CompanyPublicitaire(models.Model):
    name = models.CharField(max_length=255)  # Nom de l'entreprise
    contact_email = models.EmailField()  # Email de contact
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    platform = models.CharField(max_length=100, choices=[('Google Ads', 'Google Ads'), ('Facebook Ads', 'Facebook Ads')], default='Google Ads')
    nom_entreprise = models.CharField(max_length=255, blank=True, null=True)
   


    def __str__(self):
        return f"{self.name} ({self.nom_entreprise or 'Sans entreprise'})"
