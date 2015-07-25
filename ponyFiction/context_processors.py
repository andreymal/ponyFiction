#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings


def project_settings(request):
    return {
        'SITE_URL': settings.SITE_URL,
        'SITE_NAME': settings.SITE_NAME,
        'SITE_FEEDBACK': settings.SITE_FEEDBACK,
        'REGISTRATION_OPEN': settings.REGISTRATION_OPEN,
    }
