#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# Django
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

User = settings.AUTH_USER_MODEL


def validate_password_history(obj):
    """Here we will validate Password History count against `PASSWORD_HISTORY_LIFE`.

        - A user password history stores as per `PASSWORD_HISTORY_LIFE`.
        - If the limit has been reached then we will delete oldest Password Record so that we can store latest one.

    """
    model = obj.__class__
    pass_objects = model.objects.filter(pk=obj.id)

    # validate Password History Count
    if pass_objects.count() < getattr(settings, 'PASSWORD_HISTORY_LIFE'):
        return
    else:
        oldest_object = pass_objects.order_by('pk')[:1]  # get oldest Password object
        oldest_object.delete()  # Delete Password object.
        return


class PasswordHistory(models.Model):
    """Contains password history for user.

        - Count of Password History depends on `PASSWORD_HISTORY_LIFE` setting.
    """

    user = models.ForeignKey(User,
                             related_name="password_history",
                             on_delete=models.CASCADE)
    password = models.CharField(
        _('Password'),
        max_length=255
    )  # encrypted password
    timestamp = models.DateTimeField(
        _('Password creation Timestamp.'),
        default=timezone.now
    )  # password creation time

    class Meta:
        verbose_name = _('User Password History')
        verbose_name_plural = _('User Passwords History')

    def __str__(self):
        return '<{user}>: {timestamp}'.format(
            user=self.user,
            timestamp=self.timestamp,
        )

    def clean(self):
        """

        """
        # validate Password History
        validate_password_history(self)


class PasswordExpiry(models.Model):
    """Holds the password expiration period for a single user.

        - Password Expiry time depend on `PASSWORD_EXPIRY_TIME` setting.
    """
    user = models.OneToOneField(User,
                                related_name="password_expiry",
                                verbose_name=_("user"),
                                on_delete=models.CASCADE)
    expiry = models.PositiveIntegerField(
        _('Password expiry in days'),
        default=0)

    class Meta:
        verbose_name = _('User Password Expiry')
        verbose_name_plural = _('User Passwords Expiry')

    def __str__(self):
        return '<{user}>: {expiry}'.format(
            user=self.user,
            expiry=self.expiry,
        )