from notif.ui_notif.models import Notification
from rest_framework.serializers import ModelSerializer


# Serializers define the API representation.
class NotificationSerializer(ModelSerializer): # serializers.HyperlinkedModelSerializer):
    def update(self, instance, validated_data):
        for obj in instance:
            obj.is_read = True
            obj.save()
        return instance

    class Meta:
        model = Notification
        fields = "__all__"


class ListNotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class ReadNotificationSerializer(ModelSerializer):
    def update(self, instance, validated_data):
        instance.is_read = True
        instance.save()
        return instance

    class Meta:
        model = Notification
        fields = "__all__"



