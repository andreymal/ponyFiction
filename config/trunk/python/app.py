# -*- coding: utf-8 -*-
from ponyFiction.settings.base import *

INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
JQUERY_URL = ''

STATIC_ROOT = '/dummy'
STATIC_BASE = "https://cdn.everypony.ru/stories-trunk-static"
STATIC_VERSION = open("frontend.version").read().strip()
STATIC_URL = '{}/{}/'.format(STATIC_BASE, STATIC_VERSION)
