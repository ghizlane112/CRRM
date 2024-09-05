# notification/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Reminder, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_reminders():
    now = timezone.now()
    reminders = Reminder.objects.filter(reminder_time__lte=now, is_sent=False)

    for reminder in reminders:
        # Créez une notification pour l'utilisateur
        Notification.objects.create(
            recipient=reminder.user,
            sender=None,  # Vous pouvez définir un utilisateur si nécessaire
            message=f"Rappel: {reminder.note}",
        )
        
        # Marquez le rappel comme envoyé
        reminder.is_sent = True
        reminder.save()


@shared_task
def check_reminders():
    now = timezone.now()
    reminders = Reminder.objects.filter(reminder_time__lte=now, is_notified=False)
    
    for reminder in reminders:
        Notification.objects.create(
            recipient=reminder.user,
            sender=None,  # Vous pouvez définir un expéditeur si nécessaire
            message=reminder.note,
        )
        reminder.is_notified = True
        reminder.save()