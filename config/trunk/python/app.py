# -*- coding: utf-8 -*-
from ponyFiction.settings.base import *

INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
JQUERY_URL = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stories',
        'USER': 'celestia',
        'PASSWORD': 'solar_eclipse',
        'HOST': '127.0.0.1',
        'PORT': '4416'
    }
}
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6679',
    }
}

SITE_URL = 'https://stories-trunk.everypony.org'
SITE_NAME = 'Библиотека everypony.ru [TRUNK]'
SITE_FEEDBACK = 'https://stories-trunk.everypony.org/message'

SPHINX_CONFIG['connection_params'] = {'host': '127.0.0.1', 'port': 3401, 'charset': 'utf8'}

EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'noreply-trunk@stories.everypony.ru'

BROKER_URL = 'redis://127.0.0.1:6679/0'

CACHEOPS_REDIS = {
    'host': '127.0.0.1',
    'port': 6679,
    'socket_timeout': 3,
}

STATIC_ROOT = '/srv'
STATIC_URL = set_static_url("https://cdn.everypony.ru/stories-trunk-static")
