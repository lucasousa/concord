from concord.celery import app
from core.models import User
from django.utils import timezone
from datetime import timedelta


@app.task(bind=True)
def check_status(task_definition):
    users = User.objects.filter(
        last_ping__lte=timezone.now()-timedelta(minutes=2),
        status=User.STATUS_ONLINE
    ).update(status=User.STATUS_OFFLINE)
     
    