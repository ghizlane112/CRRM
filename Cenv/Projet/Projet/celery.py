from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projet.settings')

app = Celery('Projet')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-reminders-every-minute': {
        'task': 'notification.tasks.send_reminders',
        'schedule': crontab(minute='*/1'),  # Toutes les minutes
    },
}

