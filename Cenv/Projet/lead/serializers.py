# lead/serializers.py
from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'nom', 'prenom', 'email', 'telephone', 'source', 'statut', 'note', 'date_creation']