from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    category = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Report
        fields = ['title', 'content', 'report_type']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

    def save(self, commit=True):
        report = super().save(commit=False)
        filters = {
            'start_date': self.cleaned_data.get('start_date'),
            'end_date': self.cleaned_data.get('end_date'),
            'category': self.cleaned_data.get('category')
        }
        report.filters = {k: v for k, v in filters.items() if v is not None}
        if commit:
            report.save()
        return report
