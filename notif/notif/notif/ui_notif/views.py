from django.core.paginator import Paginator
from notif.ui_notif.models import Notification
from notif.ui_notif.api.v1.serializers import NotificationSerializer, ListNotificationSerializer, ReadNotificationSerializer

from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.status import HTTP_204_NO_CONTENT
from azure.servicebus import QueueClient
from .pagination import SmallPagesPagination, MailPaginator

User = get_user_model()


# class UiNotifyView(object):
#
#     dict_ = {}
#
#     # Create the QueueClient
#     connection_string = settings.QUEUE_CONNECTION
#
#     queue_client = QueueClient.from_connection_string(connection_string, "taskqueue06")
#
#     # Receive the message from the queue
#     with queue_client.get_receiver() as queue_receiver:
#
#         messages = queue_receiver.fetch_next()
#         for message in messages:
#
#             json = message.message.get_data()
#             print(json)
#             dict_["actor"] = json[b"actor"].decode("utf-8")
#             dict_["verb"] = json[b"verb"].decode("utf-8")
#             dict_["description"] = json[b"description"].decode("utf-8")
#             dict_["obj"] = json[b"obj"].decode("utf-8")
#
#             # get the target id
#             dict_["target"] = json[b"target"].decode("utf-8")
#             dict_["target_id"] = json[b"target_id"]
#
#             # id's for notification and actor
#             dict_["user_id"] = json[b"actor_id"]
#             dict_["notification_id"] = json[b"id"]
#
#             id_, object_ = (json[b"id"], dict_)
#
#             users = User.objects.all()
#             if len(users) == 0:
#                 user = User.objects.create_user(
#                     id=dict_["user_id"], username=object_["actor"]
#                 )
#                 user.save()
#
#                 user = User.objects.create_user(
#                     id=dict_["target_id"], username=object_["target"]
#                 )
#                 user.save()
#
#             ids = []
#             for user in users:
#                 ids.append(user.id)
#
#             if dict_["user_id"] not in ids:
#                 user = User.objects.create_user(
#                     id=dict_["user_id"], username=object_["actor"]
#                 )
#                 user.save()
#
#             if dict_["target_id"] not in ids:
#                 user = User.objects.create_user(
#                     id=dict_["target_id"], username=object_["target"]
#                 )
#                 user.save()
#
#             # create Notification model instance as notify
#             notify = Notification()
#
#             # for actor
#             notify.actor_id = object_["user_id"]
#
#             usernames = User.objects.all()
#             names = []
#             for obj in usernames:
#                 names.append(obj.username)
#
#             if object_["actor"] in names:
#                 notify.actor_type = "user"
#
#             notify.verb = object_["verb"]
#
#             # for target
#             if object_["target"] in names:
#                 notify.target_type = "user"
#             notify.target_id = object_["target_id"]
#
#             notify.description = object_["description"]
#
#             notify.save()
#
#             message.complete()


class GetNotification(ListAPIView):

    lookup_url_kwarg = "uid"
    queryset = Notification.objects.all()
    serializer_class = ListNotificationSerializer
    pagination_class = SmallPagesPagination
    ordering = ['-created']
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['actor_type', 'verb']

    def get_queryset(self):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        return self.queryset.filter(recipient_id=uid, is_read=False)


class GetAllNotification(ListAPIView):

    lookup_url_kwarg = "uid"
    queryset = Notification.objects.all()
    serializer_class = ListNotificationSerializer
    pagination_class = SmallPagesPagination
    ordering = ['-created']
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['actor_type', 'verb']

    def get_queryset(self):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        return self.queryset.filter(recipient_id=uid)


class DeleteAllNotification(APIView):
    def patch(self, request, uid):
        queryset = Notification.objects.filter(recipient_id=uid)
        for data in queryset:
            data.is_active = False
            data.save()
        return Response(status=HTTP_204_NO_CONTENT)


class DeleteNotification(DestroyAPIView):
    queryset = Notification.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active=False
        instance.save()
        return Response(status=HTTP_204_NO_CONTENT)


class ReadAllNotification(GenericAPIView):

   def patch(self, request, uid):
       page_no = request.GET.get("page")
       print(uid)
       queryset = Notification.objects.filter(recipient_id=uid)
       for data in queryset:
           data.is_read = True
           data.save()

       page = MailPaginator()
       page = page.paginate_objects(instance=queryset.values(), page_no=page_no)
       return Response(page)



class ReadNotification(UpdateAPIView):
    queryset = Notification.objects.all()
    lookup_field = 'id'
    serializer_class = ReadNotificationSerializer


class UnreadMotificationView(APIView):

    # lookup_url_kwarg = "uid"

    def get(self, request, uid):

        # uid = self.kwargs.get(self.lookup_url_kwarg)
        queryset = Notification.objects.filter(is_read=False, recipient_id=uid)
        count = queryset.count()

        top_unread = queryset.values()[:5]

        dict_ = {'count': count, 'top_unread': top_unread}

        return Response(dict_)
