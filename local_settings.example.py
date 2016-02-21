#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ponyFiction.settings.development import *


DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'local_stories',
    'USER': 'username',
    'PASSWORD': 'twilightsparkle',
    'HOST': '',
    'PORT': '',
}

SECRET_KEY = '6^j694%m%^etq6@$_d&amp;1h$fv4z4-u!#@+*m233sc-39xdac3du'

# INSTALLED_APPS += ('stories_migration',)
# TEMPLATES[0]['OPTIONS']['context_processors'] += ['stories_migration.context_processors.project_settings']
# MIGRATION_SITE = 'https://stories.everypony.ru'
# MIGRATION_NAME = 'stories.everypony.ru'

# EMAIL_PORT = 1025

# DEBUG = False
# TEMPLATE_DEBUG = False
# CACHEOPS_FAKE = False

# CACHES['default'] = {
#     'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#     'LOCATION': '127.0.0.1:11211',
# }

# CELERY_ALWAYS_EAGER = False
# SPHINX_DISABLED = False
