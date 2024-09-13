# member_management/urls.py
from django.urls import path
from . import views
from .views import delete_member

urlpatterns = [
    path('add/',views.add_member, name='add_member'),
     path('list/', views.member_list, name='member_list'),  # Ajoutez cette ligne
    path('delete-member/<int:user_id>/', delete_member, name='delete_member'),

]