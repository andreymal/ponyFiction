#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

from ponyFiction.apis.amsphinxql import SphinxPool, SphinxError

__all__ = ['SphinxError', 'sphinx']

sphinx = SphinxPool(settings.SPHINX_CONFIG['connection_params'])
