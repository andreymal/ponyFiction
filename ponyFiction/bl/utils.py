#!/usr/bin/env python
# -*- coding: utf-8 -*-

import weakref


class Resource:
    resource_name = None

    def __init__(self, resource_name):
        self.resource_name = resource_name

    def __get__(self, instance, cls):
        target = instance or cls

        if self.resource_name not in target.__dict__:
            func = registry[self.resource_name](target)
            setattr(target, self.resource_name, func)

        return target.__dict__[self.resource_name]


class BaseBL:
    _model = None

    def __init__(self, model):
        self._model = weakref.ref(model)

    @property
    def model(self):
        return self._model()


registry = {}
