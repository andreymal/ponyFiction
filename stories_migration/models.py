#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
from hashlib import md5

from django.conf import settings
from django.db import models
from django.apps import apps


def gen_token():
    return md5((str(random.randrange(10000000)) + str(time.time())).encode('utf-8')).hexdigest()


class Migration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    auth_token = models.CharField(max_length=64, default=gen_token)
    inline_token = models.CharField(max_length=64, default=gen_token)
    approved = models.BooleanField(default=False)
