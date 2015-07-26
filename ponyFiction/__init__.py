#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .bl import init_resource_registry
from .celery import app as celery_app

init_resource_registry()
