from azure.servicebus.control_client import ServiceBusService
from azure.servicebus import ServiceBusClient
from notify.signals import notify
import factory
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from azure.servicebus import QueueClient, Message
from django.db.models.signals import post_save
from notify.models import Notification
from django.conf import settings

from azure.servicebus.control_client import ServiceBusService, Message, Topic, Rule, DEFAULT_RULE_NAME
User = get_user_model()


class SenderView(APIView):

    # creating multiple users
    user = User.objects.create_user(id=3, username="dimri")
    user.save()

    user1 = User.objects.create_user(id=2, username="archan")
    user1.save()

    user2 = User.objects.create_user(id=4, username="ketul")
    user2.save()

    # some factory introduction
    verb = factory.Faker("sentence").generate()
    nf_type = factory.Faker("sentence").generate()

    actor_text = factory.Faker("text").generate()
    description = factory.Faker("text").generate()

    # Send a test message to the queue
    msg = notify.send(
        user,
        recipient=user1,
        actor=user,
        actor_text=actor_text,
        verb=verb,
        nf_type=nf_type,
        target=user2,
        obj=user1,
    )

    bus_service = ServiceBusService(
        service_namespace='topicsubscriptionbus',
        shared_access_key_name='RootManageSharedAccessKey',
        shared_access_key_value='H8Efc9zcWcwQlElWrtwRa6cxyYI+QUCfnqyUmYudP6o=')

    bus_service.delete_topic("mytopic")
    bus_service.create_topic('mytopic')

    topic_options = Topic()
    topic_options.max_size_in_megabytes = '5120'
    topic_options.default_message_time_to_live = 'PT1M'

    bus_service.create_topic('mytopic', topic_options)

    bus_service.create_subscription('mytopic', 'AllMessages')

    # looking for the matching notification
    notification = Notification.objects.get(verb=verb)
    data = notification.as_json()

    des = data["actor"] + " is performing task on " + data["target"]
    data["description"] = des

    actor_name = data["actor"]
    # recipient_name = data['recipient']
    target_name = data["target"]

    user = User.objects.get(username=actor_name)
    data["actor_id"] = user.id

    user = User.objects.get(username=target_name)
    data["target_id"] = user.id

    # creating a message to be send to the message queue
    object = Message(data)

    bus_service.send_topic_message('mytopic', object)


# class SenderView(APIView):
#
#     # Service Bus primary connection string value
#     connection_string = settings.QUEUE_CONNECTION
#
#     # creating the ServiceBusClient object
#     sb_client = ServiceBusClient.from_connection_string(connection_string)
#
#     """
#     must delete the queue berfore you use it as it might throw you the error
#     with multiple operation done simultaneously on a queue you created.
#     """
#     sb_client.delete_queue("taskqueue06")
#
#     # creating the mesage queue
#     sb_client.create_queue("taskqueue06")
#
#     # creating multiple users
#     user = User.objects.create_user(id=3, username="dimri")
#     user.save()
#
#     user1 = User.objects.create_user(id=2, username="archan")
#     user1.save()
#
#     user2 = User.objects.create_user(id=4, username="ketul")
#     user2.save()
#
#     # Create the QueueClient
#     queue_client = QueueClient.from_connection_string(connection_string, "taskqueue06")
#
#     # some factory introduction
#     verb = factory.Faker("sentence").generate()
#     nf_type = factory.Faker("sentence").generate()
#
#     actor_text = factory.Faker("text").generate()
#     description = factory.Faker("text").generate()
#
#     # Send a test message to the queue
#     msg = notify.send(
#         user,
#         recipient=user1,
#         actor=user,
#         actor_text=actor_text,
#         verb=verb,
#         nf_type=nf_type,
#         target=user2,
#         obj=user1,
#     )
#
#     # looking for the matching notification
#     notification = Notification.objects.get(verb=verb)
#     data = notification.as_json()
#
#     des = data["actor"] + " is performing task on " + data["target"]
#     data["description"] = des
#
#     actor_name = data["actor"]
#     # recipient_name = data['recipient']
#     target_name = data["target"]
#
#     user = User.objects.get(username=actor_name)
#     data["actor_id"] = user.id
#
#     user = User.objects.get(username=target_name)
#     data["target_id"] = user.id
#
#     # creating a message to be send to the message queue
#     object = Message(data)
#
#     # sending the message object
#     queue_client.send(object)
