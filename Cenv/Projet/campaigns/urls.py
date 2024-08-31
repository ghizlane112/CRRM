
from django.urls import path
from . import views

urlpatterns = [
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('add-campaign/', views.add_campaign, name='add_campaign'),
]
