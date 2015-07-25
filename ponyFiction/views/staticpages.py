#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from ponyFiction.models import StaticPage


def view(request, name):
    page = get_object_or_404(StaticPage, name=name)
    return render(request, 'staticpage.html', {'page': page})
