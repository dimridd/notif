from celery import shared_task
from .views import UiNotifyView


@shared_task(name="notif")
def receive_notification():

	UiNotifyView()
