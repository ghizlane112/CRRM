# member_management/forms.py
from django import forms
from users.models import Users
from django.contrib.auth.forms import UserCreationForm

class MemberCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=[('user', 'Utilisateur Normal'), ('admin', 'Administrateur')],
        required=True,
        label='Type d\'utilisateur'
    )

    class Meta:
        model = Users
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data['user_type']
        if user_type == 'admin':
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
        if commit:
            user.save()
        return user