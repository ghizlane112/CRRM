from django.db import models
# models.py
from lead.models import Lead
from Rendez.models import Event
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.recipient.username} from {self.sender.username}'



class Reminder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    note = models.TextField()

    def __str__(self):
        return f"Rappel pour {self.event.title} le {self.reminder_time}"