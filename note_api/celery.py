import os
import settings
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'note_api.settings')

app = Celery('note_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'checkVotes': {
        'task': 'data.tasks.checkVotes',
        'schedule': crontab(minute='*/1')

    },
    'calcStats': {
            'task': 'data.tasks.calcStats',
            'schedule': crontab(minute='*/5')

    },
    'resetClaim': {
        'task': 'user.tasks.resetClaim',
        'schedule': crontab(minute=0, hour='*/6')
    },
}
