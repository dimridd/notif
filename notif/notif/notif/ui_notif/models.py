from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from notif.core.behaviours import StatusMixin

# Create your models here.


@python_2_unicode_compatible
class Notification(StatusMixin, TimeStampedModel):

    LEVEL_CHOICES = (
        ("INFO", "info"),
        ("SUCCESS", "success"),
        ("WARNING", "warning"),
        ("ERROR", "error"),
    )

    level = models.CharField(
        max_length=255, choices=LEVEL_CHOICES, blank=True, null=True
    )

    is_read = models.BooleanField(_("mark"), null=False, blank=False, default=True)

    ACTOR_TYPE = (("SERVICE", "service"), ("USER", "user"))

    actor_type = models.CharField(
        max_length=255, choices=ACTOR_TYPE, blank=True, null=True
    )

    actor_id = models.CharField(
        _("actor short ID"), blank=True, null=True, max_length=255
    )

    RECIPIENT_TYPE = (("SERVICE", "service"), ("USER", "user"))

    recipient_type = models.CharField(
        max_length=255, choices=RECIPIENT_TYPE, blank=True, null=True
    )

    recipient_id = models.CharField(
        _("recipient short ID"), blank=True, null=True, max_length=255
    )

    verb = models.TextField(_("Action Description"), blank=True, null=True)

    NF_TYPE = (("UI", "ui"), ("EMAIL", "email"), ("SERVICE", "service"))

    nf_type = models.CharField(
        max_length=255, choices=NF_TYPE, blank=True, null=True
    )

    description = models.TextField(_("Notification Description"), blank=True, null=True)

    TARGET_TYPE = (("OBJ", "object"), ("IMG", "image"), ("URL", "url"))

    target_type = models.CharField(
        max_length=255, choices=TARGET_TYPE, blank=True, null=True
    )

    target = models.URLField(
        _("target url"), blank=True, null=True, max_length=255
    )

    deletd_by = models.CharField(
        _("user ID"), blank=True, null=True, max_length=255
    )

    retry_action = models.CharField(
        _("retry action"), blank=True, null=True, max_length=255
    )

    retry_log = models.CharField(
        _("retry action"), blank=True, null=True, max_length=255
    )

    retry_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.verb

