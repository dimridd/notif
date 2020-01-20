from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("reciever", result_backend="amqp://localhost//")

app.conf.beat_schedule = {
    # name of the scheduler

    'add-every-5-seconds': {
        # task name which we have created in tasks.py

        'task': 'notif',
        # set the period of running

        'schedule': 12.0,

    },
}

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
