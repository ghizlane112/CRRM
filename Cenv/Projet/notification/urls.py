# notification/urls.py
from django.urls import path
from . import views
from Rendez.views import calendar_view

urlpatterns = [
     path('notifications/', views.notifications, name='notifications'),
   # path('reminders/', views.list_reminders, name='list_reminders'),
    path('reminder/new/', views.create_reminder, name='create_reminder'),
    #path('reminder/new/<int:lead_id>/', views.create_reminder, name='create_reminder'),
    path('calendar/', calendar_view, name='calendar'),  # Ajoutez cette ligne

]
