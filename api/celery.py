from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordanalyzer.settings')

app = Celery('wordanalyzer')

# Use Redis as the Celery message broker.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(BROKER_URL='redis://localhost:6379/0')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task
def process_input_task(input_type, input_data):
    from api.word_counter.src.services.word_counter_service import WordCounterService
    WordCounterService.process_input(input_type, input_data)
