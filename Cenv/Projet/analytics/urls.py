# analyse/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('lead-status-data/', views.lead_status_data, name='lead_status_data'),
    path('lead-source-data/', views.lead_source_data, name='lead_source_data'),
    path('lead-conversion-data/', views.lead_conversion_data, name='lead_conversion_data'),
    path('conversion-report/', views.conversion_report_view, name='conversion_report_data'),
    path('', views.analytics_view, name='analytics_view'),
]
