from django import forms
from .models import CompanyPublicitaire
from lead.models import Lead  # Import du modèle Lead

class CampaignForm(forms.ModelForm):
    # Utiliser une liste déroulante pour les leads
    leads = forms.ModelMultipleChoiceField(
        queryset=Lead.objects.filter(is_deleted=False),  # Exclure les leads supprimés
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),  # Sélection multiple
        required=False,
        label='Leads associés'
    )

    class Meta:
        model = CompanyPublicitaire
        fields = ['name', 'contact_email', 'start_date', 'end_date', 'budget', 'nom_entreprise', 'leads']



        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()  # Sauvegarder les relations Many-to-Many
        return instance
