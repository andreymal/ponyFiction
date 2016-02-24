# -*- coding: utf-8 -*-

from ponyFiction.settings.base import *

INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
