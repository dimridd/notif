# -*- coding: utf-8 -*-
# Stdlib imports
from __future__ import unicode_literals, absolute_import

# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Local imports
from .managers import StatusMixinManager


class StatusMixin(models.Model):
    """
    Holds and manages active and deleted state for the object.
    Also provide created and modified fields from TimeStampedModel
    """

    is_active = models.BooleanField(_("Active"), default=True, blank=False, null=False)
    is_deleted = models.BooleanField(
        _("Deleted"), default=False, blank=False, null=False
    )

    objects = StatusMixinManager()

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save()

    def remove(self):
        if not self.is_deleted:
            self.is_deleted = True
            self.save()

    def has_changed(self, field):
        model = self.__class__.__name__
        return getattr(self, field) != getattr(
            self, "_" + model + "__original_" + field
        )

    def save(self, *args, **kwargs):
        """
        Makes sure that the ``is_active`` is ``False`` when ``is_deleted`` is ``True``.
        """
        if self.is_deleted:
            self.is_active = False
        super(StatusMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
