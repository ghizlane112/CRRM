from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.core.mail import send_mail
from .models import Notification
from .models import Reminder

@shared_task
def send_reminders():
    now = timezone.now()
    reminders = Notification.objects.filter(reminder_time__lte=now, is_read=False)
    
    for reminder in reminders:
        send_mail(
            'Rappel',
            reminder.message,
            'from@example.com',  # L'adresse de l'expéditeur
            [reminder.recipient.email],
            fail_silently=False,
        )
        reminder.is_read = True  # Marquer le rappel comme envoyé
        reminder.save()
