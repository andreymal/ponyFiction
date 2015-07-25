#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template

from ponyFiction.models import HtmlBlock

register = template.Library()


@register.simple_tag
def html_block(name):
    block = HtmlBlock.objects.filter(name=name).cache().first()
    return block.content if block else ''
