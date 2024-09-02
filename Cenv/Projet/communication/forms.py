from django import forms
from .models import Message
from .models import Document
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageForm(forms.ModelForm):
     class Meta:
         model = Message
         fields = ['receiver', 'lead', 'content']
         widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }





class DocumentForm(forms.ModelForm):
    shared_with = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Partager avec"
    )

    class Meta:
        model = Document
        fields = ['file', 'description', 'shared_with']
