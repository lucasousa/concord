from datetime import timedelta

from concord.celery import app
from django.utils import timezone

from core.models import User


@app.task(bind=True)
def check_status(task_definition):
    users = User.objects.filter(
        last_ping__lte=timezone.now() - timedelta(minutes=2), status=User.STATUS_ONLINE
    ).update(status=User.STATUS_OFFLINE)
