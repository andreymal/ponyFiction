#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .utils import BaseBL


class NewsItemBL(BaseBL):
    def suggest(self):
        return self.model.objects.filter(visible=True).order_by('-updated').cache().first()
