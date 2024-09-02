from django.urls import path
from .views import inbox, send_message
from . import views

urlpatterns = [
    path('inbox/', inbox, name='inbox'),
    path('send_message/', send_message, name='send_message'),
    path('lead/<int:pk>/upload-document/', views.upload_document, name='upload_document'),
]