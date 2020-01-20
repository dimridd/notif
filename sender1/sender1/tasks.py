from celery import shared_task
from .views import SenderView


@shared_task
def send_notification():

    SenderView()

