from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime 
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def clean(self):
        if self.birth_date and self.birth_date > datetime.date.today():
            raise ValidationError('La date de naissance ne peut pas être dans le futur.')
