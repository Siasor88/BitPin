from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('post_rating_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_post_aggregates_every_minute': {
        'task': 'kafka_agents.tasks.update_post_aggregates_task',
        'schedule': crontab(minute='*/1'),  # Every 1 minute
    },
}
