import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailbox_api.settings')

app = Celery('mailbox_api')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
