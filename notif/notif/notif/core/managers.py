# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db.models import Manager


class StatusMixinManager(Manager):
    def all(self, *args, **kwargs):
        return super(StatusMixinManager, self).filter(is_deleted=False)

    def filter(self, *args, **kwargs):
        return (
            super(StatusMixinManager, self)
            .filter(is_active=True, is_deleted=False)
            .filter(*args, **kwargs)
        )

    def active(self, *args, **kwargs):
        return super(StatusMixinManager, self).filter(is_active=True, is_deleted=False)
