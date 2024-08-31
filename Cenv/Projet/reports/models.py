from django.db import models

# Create your models here.
from django.db import models
#from django.contrib.auth.models import User
from datetime import date, datetime
import json
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('conversion', 'Rapport de Conversion'),
        ('campaign_performance', 'Rapport de Performance des Campagnes'),
        ('interaction', 'Rapport de Suivi des Interactions'),
    ]
     
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=100, choices=REPORT_TYPE_CHOICES)
    filters = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='')
   
    def _str_(self):
        return f"{self.title} ({self.get_report_type_display()})"
    

    def filters_summary(self):
        if not self.filters:
            return "Aucun filtre appliqué"

        def convert(value):
            if isinstance(value, (datetime, date)):
                return value.strftime('%Y-%m-%d')  # Format pour les dates
            return value
        
        summary = []
        for key, value in self.filters.items():
            if isinstance(value, list):
                value = ', '.join(map(str, value))
            elif isinstance(value, (datetime, date)):
                value = convert(value)
            summary.append(f"{key.replace('_', ' ').capitalize()}: {value}")
        return "; ".join(summary)  