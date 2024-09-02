from django import forms
from .models import Lead, Note
import csv
from io import StringIO
from .models import Interaction
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
#from .models import Interaction


# lead/forms.py
class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['nom', 'prenom', 'email', 'telephone', 'source', 'note', 'responsable']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_superuser:
            # Pour les admins, afficher uniquement les utilisateurs normaux (non-admins)
            self.fields['responsable'].queryset = User.objects.filter(is_superuser=False)
        else:
            # Pour les utilisateurs normaux, cacher le champ 'responsable' et l'assigner automatiquement
            self.fields['responsable'].widget = forms.HiddenInput()
            if self.instance and self.instance.pk is None:
                self.initial['responsable'] = user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.pk:
            if Lead.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Un lead avec cet email existe déjà.")
        else:
            if Lead.objects.filter(email=email).exists():
                raise forms.ValidationError("Un lead avec cet email existe déjà.")
        return email


class LeadSortForm(forms.Form):
    SORT_CHOICES = [
        ('first_name', 'Prénom'),
        ('last_name', 'Nom'),
        ('email', 'Email'),
        ('phone', 'Téléphone'),
        ('source', 'Source'),
        ('status', 'Statut'),
        ('created_at', 'Date de création'),
    ]
    ordering = forms.ChoiceField(choices=SORT_CHOICES, required=True, label='Trier par')



class CSVImportForm(forms.Form):
   csv_file = forms.FileField()
   
   def handle_uploaded_file(self, file, user):
        file_content = file.read().decode('utf-8')
        csv_file = StringIO(file_content)
        reader = csv.DictReader(csv_file)
        for row in reader:
            Lead.objects.create(
                nom=row['nom'],
                prenom=row['prenom'],
                email=row['email'],
                telephone=row['telephone'],
                source=row['source'],
                statut=row['statut'],
                note=row.get('note', ''),
                responsable=user  # Assigner l'utilisateur qui importe
            )




#class InteractionForm(forms.ModelForm):
 #   class Meta:
  #      model = Interaction
   #     fields = ['type', 'date', 'description', 'lead', 'user']


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['lead', 'type_interaction', 'date_interaction', 'note']
        widgets = {
            'date_interaction': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }



class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']