#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS' : False}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = ()

SECRET_KEY = '6^j694%m%^etq6@$_d&amp;1h$fv4z4-u!#@+*m233sc-39xdac3du'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)
ROOT_URLCONF = 'ponyFiction.urls'
ALLOWED_HOSTS = ['*']
WSGI_APPLICATION = 'ponyFiction.wsgi.application'

NSFW_RATING_IDS = (1,)

# Application definition

INSTALLED_APPS = (
    'cacheops',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'stories_migration',
    'ponyFiction',
    'django.contrib.admin',
    'ponyFiction.apis.captcha',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

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
    'server' : ('/tmp/sphinx.socket',),
    'retries_count' : 5,
    'retries_delay' : 1,
    'timeout' : 10,
    'match_mode' : 0,  # SPH_MATCH_ALL,
    'rank_mode' : 0,  # SPH_RANK_SPH04,
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
COMMENT_MIN_LENGTH = 1
BRIEF_COMMENT_LENGTH = 100

RSS = {'stories': 20, 'chapters': 20, 'comments': 100}

AUTH_USER_MODEL = 'ponyFiction.Author'
AUTHENTICATION_BACKENDS = ('ponyFiction.auth_backends.AuthorModelBackend',)
ACCOUNT_ACTIVATION_DAYS = 5
REGISTRATION_AUTO_LOGIN = True
REGISTRATION_FORM = 'ponyFiction.forms.register.AuthorRegistrationForm'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'noreply@stories.everypony.ru'

RECAPTCHA_PUBLIC_KEY = '6LfbstoSAAAAAAcFIteoZTld24mt3s6_sODZnc8J'
RECAPTCHA_PRIVATE_KEY = '6LfbstoSAAAAAHHN9jYw9Lp9lsunQCILAyAYgoxz'
RECAPTCHA_USE_SSL = True
NOCAPTCHA = True


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
    'blockquote', 'sup', 'sub', 'pre', 'small', 'tt', 'font',
]

CHAPTER_ALLOWED_ATTRIBUTES = {
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'a': ['href', 'rel', 'title'],
    'span': ['align'],
    'p': ['align'],
    'footnote': ['id'],
    'font': ['size', 'color'],
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

PUBLISH_SIZE_LIMIT = 1000

STORY_DOWNLOAD_FORMATS = reversed((
    'ponyFiction.downloads.fb2.FB2Download',
    'ponyFiction.downloads.html.HTMLDownload',
    # 'ponyFiction.downloads.txt.TXTDownload',
    # 'ponyFiction.downloads.txt.TXT_CP1251Download',
))


CACHEOPS_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'socket_timeout': 3,
}

CACHEOPS_DEFAULTS = {
    'timeout': 3600
}

CACHEOPS = {
    'auth.user': {'ops': 'get', 'timeout': 60 * 15},
    'ponyFiction.Story': {'ops': 'get', 'timeout': 3600 * 3},
    'ponyFiction.Chapter': {'ops': 'get', 'timeout': 3600 * 3},
    'ponyFiction.Comment': {'ops': 'get', 'timeout': 3600 * 3},
    
    'ponyFiction.Character': {'ops': 'all', 'timeout': 3600 * 24 *30},
    'ponyFiction.Category': {'ops': 'all', 'timeout': 3600 * 24 *30},
    'ponyFiction.Classifier': {'ops': 'all', 'timeout': 3600 * 24 * 30},
    'ponyFiction.Rating': {'ops': 'all', 'timeout': 3600 * 24 * 30},
    
    'auth.*': {'ops': 'all', 'timeout': 3600},
    '*.*': {'ops': 'just_enable', 'timeout': 3600},
}


REGISTRATION_OPEN = True
LOAD_TABUN_AVATARS = True


# specify current environment

ENV = os.getenv('DJANGO_ENV')
if not ENV:
    ENV = open(os.path.join(BASE_DIR, 'environment.txt'), 'rb').read().strip().decode('utf-8', 'replace')

if ENV in ('test', 'development', 'staging', 'production'):
    env_path = os.path.join(PROJECT_DIR, 'environments', ENV + '.py')
    if os.path.isfile(env_path):
        exec(open(env_path, 'rb').read())

local_path = os.path.join(PROJECT_DIR, 'environments', 'local.py')
if os.path.isfile(local_path):
    exec(open(local_path, 'rb').read())
