from django.urls import path
from . import views

urlpatterns = [
    path('calendar_view', views.calendar_view, name='calendar_view'),  # La vue principale pour /event
    path('events/', views.event_list, name='event_list'), 
    path('add-event/', views.add_event, name='add_event'),
    path('history/', views.history_view, name='history_view'),  # Nouvelle URL pour l'historique
    path('update-event/', views.update_event, name='update_event'),
    path('delete-event/', views.delete_event, name='delete_event'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'), # L'URL pour obtenir les événements
   
    path('<int:event_id>/', views.event_detail, name='event_detail'),  # Nouvelle URL pour les détails
   
]
