from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','Ecommerce.settings')

app = Celery('Ecommerce')

app.config_from_object('django.conf:settings',namespace='CELERY') 

app.autodiscover_tasks() 

app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {
    'check-inventory': {
        'task': 'Ecommerce.tasks.check_inventory',
        'schedule': 3600.0,
    },
    'clear-reservations': {
        'task': 'Ecommerce.tasks.check_cart_expirations',
        'schedule': 30.0
    },
}