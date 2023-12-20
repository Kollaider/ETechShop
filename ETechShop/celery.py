from django.conf import settings

import os
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ETechShop.settings')

app = Celery("ETechShop")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'increase_debts_every_3_hours': {
        'task': 'webapp.tasks.increase_debt',
        'schedule': timedelta(hours=3),
    },
    'decrease_debts_every_at_6_30': {
        'task': 'webapp.tasks.debt_reduction',
        'schedule': crontab(hour=14, minute=18),
    },
}
app.conf.timezone = 'UTC'
