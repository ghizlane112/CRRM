# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Reminder

@shared_task
def send_reminders():
    now = timezone.now()
    reminders = Reminder.objects.filter(reminder_time__lte=now, reminder_time__gte=now - timezone.timedelta(hours=24), is_read=False)

    for reminder in reminders:
        send_mail(
            'Rappel de Rendez-vous',
            f'Vous avez un rendez-vous avec {reminder.lead.nom} le {reminder.reminder_time}. Note: {reminder.note}',
            'from@example.com',  # Adresse de l'expéditeur
            [reminder.user.email],
            fail_silently=False,
        )
        reminder.is_read = True  # Marquer le rappel comme envoyé
        reminder.save()
