# -*- coding: utf-8 -*-

from ponyFiction.settings.base import *

INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES
JQUERY_URL = ''

# Captcha
RECAPTCHA_PUBLIC_KEY = '6Ld1_QgUAAAAAMh-JiWgux_6CERc4aATQs0iK-J2'
RECAPTCHA_PRIVATE_KEY = '6Ld1_QgUAAAAAAAAmZSDhjvskUNHFsZniIdwkn5S'

# Templates
TEMPLATES[0]['OPTIONS']['loaders'] = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]
