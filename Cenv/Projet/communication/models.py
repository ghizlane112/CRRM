from django.db import models

# Create your models here.
from django.db import models
from lead.models import Lead
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages',null=True, blank=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} on {self.timestamp}"
    

