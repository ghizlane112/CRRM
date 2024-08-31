from django.urls import path
from .views import inbox, send_message

urlpatterns = [
    path('inbox/', inbox, name='inbox'),
    path('send_message/', send_message, name='send_message'),
    
]