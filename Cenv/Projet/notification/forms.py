from django import forms
from .models import Reminder

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['event', 'reminder_time', 'note']
        widgets = {
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
