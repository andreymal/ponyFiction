#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings


def project_settings(request):
    return {
        'MIGRATION_SITE': settings.MIGRATION_SITE,
        'MIGRATION_NAME': settings.MIGRATION_NAME,
    }
