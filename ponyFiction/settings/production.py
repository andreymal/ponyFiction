# -*- coding: utf-8 -*-

from ponyFiction.settings.base import *


CACHES['default'] = {
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
}

SITE_URL = 'https://stories.everypony.ru'
