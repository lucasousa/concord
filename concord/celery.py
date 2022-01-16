import os
from celery import Celery
from django.conf import settings 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concord.settings')
app = Celery('concord')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Scheduling tasks
# app.conf.beat_schedule = {
#     'check_status': {
#         'task': 'core.tasks.check_status',
#         'schedule': 20.0,
#     },
# }

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


