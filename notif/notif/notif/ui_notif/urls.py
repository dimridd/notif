from django.urls import path
from notif.ui_notif import views
from notif.ui_notif.views import ReadAllNotification, DeleteNotification, GetNotification, \
    GetAllNotification, ReadNotification, DeleteAllNotification, UnreadMotificationView

urlpatterns = [
    path("getNotification/<uid>", GetNotification.as_view(), name="getNotification"),
    path("getAllNotification/<uid>", GetAllNotification.as_view(), name="getAllNotification"),

    path("deleteNotification/<int:id>/", DeleteNotification.as_view(), name="deleteNotification"),
    path("deleteAllNotification/<uid>", DeleteAllNotification.as_view(), name="deleteAllNotification"),

    path("readNotification/<id>", ReadNotification.as_view(), name="readNotification"),
    path("readAllNotification/<uid>", ReadAllNotification.as_view(), name="readAllNotification"),

    path("unreadCount/<uid>", UnreadMotificationView.as_view(), name="unreadCount"),
]
