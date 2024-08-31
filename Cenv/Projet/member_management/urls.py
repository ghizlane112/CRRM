# member_management/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.add_member, name='add_member'),
     path('list/', views.member_list, name='member_list'),  # Ajoutez cette ligne
]