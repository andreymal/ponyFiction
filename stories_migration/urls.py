#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import new, approve

urlpatterns = patterns('',
  url(r'^$', new, name='migration_new'),
  url(r'^(?P<auth_token>\w+)/$', approve, name='migration_approve')
)
