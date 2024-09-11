# rendez/urls.py
from django.urls import path
from .views import book_appointment,appointment_success

urlpatterns = [
    path('book-appointment/', book_appointment, name='book_appointment'),
   path('appointment-success/', appointment_success, name='appointment_success'),

    # autres URL...
]
