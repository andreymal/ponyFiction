# -*- coding: utf-8 -*-
# Django settings for ponyFiction project.
import os
from ponyFiction.apis.sphinxapi import SPH_MATCH_ALL, SPH_RANK_SPH04

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS' : False}
MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fanfics',
        'USER': 'fanfics',
        'PASSWORD': 'twilightsparkle',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), os.pardir, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '6^j694%m%^etq6@$_d&amp;1h$fv4z4-u!#@+*m233sc-39xdac3du'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#    'django.template.loaders.eggs.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)
ROOT_URLCONF = 'ponyFiction.urls'
ALLOWED_HOSTS = ['*']
WSGI_APPLICATION = 'ponyFiction.wsgi.application'

import os.path
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\', '/'),
)

INSTALLED_APPS = (
    'cacheops',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'ponyFiction',
    'django.contrib.admin',
    'debug_toolbar',
    'registration',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)
COMPRESS_HTML = True
SPHINX_CONFIG = {
    'server' : '/tmp/sphinx.socket',
    'retries_count' : 5,
    'retries_delay' : 1,
    'timeout' : 10,
    'match_mode' : SPH_MATCH_ALL,
    'rank_mode' : SPH_RANK_SPH04,
    'number' : 10,
    'max' : 1000,
    'cutoff' : 1000,
    'excerpts_opts' : {'chunk_separator' : '…', 'limit' : 2048, 'around' : 10, 'html_strip_mode' : 'strip'},
    'weights_stories' : {'title' : 100, 'summary' : 50, 'notes' : 25, 'username': 150},
    'weights_chapters' : {'text' : 100, 'title' : 50, 'notes' : 25}
    }
COMMENTS_COUNT = {
                  'page' : 50,
                  'main' : 5,
                  'stream' : 50,
                  'author_page': 10
                  }
STORIES_COUNT = {'page' : 10, 'main' : 10, 'stream' : 20}
CHAPTERS_COUNT = {'page' : 10, 'main' : 10, 'stream' : 20}
COMMENTS_ORPHANS = 5
COMMENT_MIN_LENGTH = 0
BRIEF_COMMENT_LENGTH = 100
RSS = {'stories': 20, 'chapters': 20, 'comments': 100}
AUTH_USER_MODEL = 'ponyFiction.Author'
AUTHENTICATION_BACKENDS = ('ponyFiction.auth_backends.AuthorModelBackend',)
ACCOUNT_ACTIVATION_DAYS = 5
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'noreply@stories.everypony.ru'
RECAPTCHA_PUBLIC_KEY = '6LfbstoSAAAAAAcFIteoZTld24mt3s6_sODZnc8J'
RECAPTCHA_PRIVATE_KEY = '6LfbstoSAAAAAHHN9jYw9Lp9lsunQCILAyAYgoxz'
ALLOWED_TAGS = [
    'b', 'i', 'strong', 'em', 's', 'u',
    'p', 'br', 'hr',
    'a',
    'ul', 'ol', 'li',
    'blockquote', 'sup', 'sub', 'pre', 'small', 'tt'
]

ALLOWED_ATTRIBUTES = {
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'a': ['href', 'rel', 'title'],
}

CHAPTER_ALLOWED_TAGS = [
    'b', 'i', 'strong', 'em', 's', 'u',
    'h3', 'h4', 'h5',
    'p', 'span', 'br', 'hr', 'footnote',
    'img', 'a',
    'ul', 'ol', 'li',
    'blockquote', 'sup', 'sub', 'pre', 'small', 'tt'
]

CHAPTER_ALLOWED_ATTRIBUTES = {
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'a': ['href', 'rel', 'title'],
    'span': ['align'],
    'p': ['align'],
	'footnote': ['id'],
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

PUBLISH_SIZE_LIMIT = 1000

STORY_DOWNLOAD_FORMATS = reversed((
    'ponyFiction.downloads.fb2.FB2Download',
    'ponyFiction.downloads.html.HTMLDownload',
    # 'ponyFiction.downloads.txt.TXTDownload',
    # 'ponyFiction.downloads.txt.TXT_CP1251Download',
))

try:
    from local_settings import *
except ImportError:
    pass

CACHEOPS_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'socket_timeout': 3,
}
CACHEOPS = {
    'auth.user': ('get', 60*15),
    'ponyFiction.Story': ('get', 60*60*3),
    'ponyFiction.Chapter': ('get', 60*60*3),
    'ponyFiction.Comment': ('get', 60*60*3),
    
    'ponyFiction.Character': ('all', 60*60*24*30),
    'ponyFiction.Category': ('all', 60*60*24*30),
    'ponyFiction.Classifier': ('all', 60*60*24*30),
    'ponyFiction.Rating': ('all', 60*60*24*30),
    
    'auth.*': ('all', 60*60),
    '*.*': ('just_enable', 60*60),
}
