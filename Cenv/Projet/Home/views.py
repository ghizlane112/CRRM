from django.shortcuts import render

# Create your views here.
# home/views.py
from django.shortcuts import render, redirect
from .forms import AppointmentForm
from notification.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Save the appointment
            appointment = form.save()

            # Create notifications for admins
            admins = User.objects.filter(is_staff=True)  # Assuming staff users are admins
            for admin in admins:
                Notification.objects.create(
                    recipient=admin,
                    sender=request.user if request.user.is_authenticated and isinstance(request.user, User) else None,  # Check if the user is authenticated and of type User
                    appointment=appointment,
                    message=f"Nouvelle réservation de rendez-vous:\n"
                            f"Nom: {appointment.nom} {appointment.prenom}\n"
                            f"Email: {appointment.email}\n"
                            f"Téléphone: {appointment.phone}\n"
                            f"Date: {appointment.appointment_date}\n"
                            f"Lieu: {appointment.lieu}\n"
                            f"Message: {appointment.message}"
                )

            # Redirect to success page after saving
            return redirect('appointment_success')
    else:
        form = AppointmentForm()

    return render(request, 'appointment_form.html', {'form': form})

def appointment_success(request):
    return render(request, 'appointment_success.html')
