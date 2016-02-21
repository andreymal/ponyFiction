# -*- coding: utf-8 -*-

from django.apps import AppConfig


class PonyFictionConfig(AppConfig):
    name = 'ponyFiction'

    def ready(self):
        from .bl import init_resource_registry
        from .celery import app as celery_app

        init_resource_registry()
