
from django.urls import path
from . import views

urlpatterns = [
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('add-campaign/', views.add_campaign, name='add_campaign'),
 path('export-campaigns/', views.export_campaigns, name='export_campaigns'),  # Vérifiez cette ligne
  path('export-campaigns-pdf/', views.export_campaigns_pdf, name='export_campaigns_pdf'),  # Ajoutez cette ligne
 ]
