#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery
from django.conf import settings

app = Celery('ponyFiction')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
