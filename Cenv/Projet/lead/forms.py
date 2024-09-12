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
    raison = forms.CharField(required=False, widget=forms.Textarea, label='Raison')

    class Meta:
        model = Lead
        fields = ['nom', 'prenom', 'email', 'telephone', 'source', 'note', 'responsable', 'statut', 'raison']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Masquer le champ 'responsable' pour les utilisateurs non super-utilisateurs
        if user and user.is_superuser:
            self.fields['responsable'].queryset = User.objects.filter(is_superuser=False)
        else:
            self.fields.pop('responsable', None)  # Retirer le champ 'responsable'

        # Ajouter le champ 'statut' si le lead existe déjà
        if self.instance and self.instance.pk:
            self.fields['statut'].required = True
        else:
            self.fields.pop('statut', None)

        # Afficher ou masquer le champ 'raison' en fonction du statut
        if self.instance and self.instance.statut == 'Perdu':
            self.fields['raison'].widget.attrs['style'] = 'display: block;'
        else:
            self.fields['raison'].widget.attrs['style'] = 'display: none;'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.pk:
            if Lead.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Un lead avec cet email existe déjà.")
        else:
            if Lead.objects.filter(email=email).exists():
                raise forms.ValidationError("Un lead avec cet email existe déjà.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        statut = cleaned_data.get('statut')
        raison = cleaned_data.get('raison')

        if statut == 'Perdu' and not raison:
            self.add_error('raison', 'La raison est requise lorsque le statut est "Perdu".')

        return cleaned_data






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



class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['type_interaction', 'date_interaction','content']
        widgets = {
            'date_interaction': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }





class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 10, 'placeholder': 'Entrez votre note ici...'}),
        }