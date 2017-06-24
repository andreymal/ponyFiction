#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps


class AuthorModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = self.user_class.objects.get(username=username)
            if user.check_password(password):
                return user
        except self.user_class.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            # pylint: disable=attribute-defined-outside-init
            self._user_class = apps.get_model(settings.AUTH_USER_MODEL)
            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model')
        return self._user_class
