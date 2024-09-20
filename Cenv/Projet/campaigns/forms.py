from django import forms
from .models import CompanyPublicitaire
from lead.models import Lead

class CampaignForm(forms.ModelForm):
    leads = forms.ModelMultipleChoiceField(
        queryset=Lead.objects.filter(is_deleted=False),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'}),  # Taille augmentée pour plus de visibilité
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
            self.save_m2m()
        return instance
