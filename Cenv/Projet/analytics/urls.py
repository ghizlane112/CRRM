# analyse/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('lead-status-data/', views.lead_status_data, name='lead_status_data'),
]
