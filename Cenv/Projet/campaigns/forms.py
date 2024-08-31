from django import forms
from .models import CompanyPublicitaire

class CampaignForm(forms.ModelForm):
    class Meta:
        model = CompanyPublicitaire
        fields = ['name', 'contact_email', 'start_date', 'end_date', 'budget', 'nom_entreprise']
