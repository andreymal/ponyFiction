# -*- coding: utf-8 -*-
from django import template
from ponyFiction.utils.typographus import typo
register = template.Library()

@register.filter
def typogrify(string):
    if type(string) is not unicode:
        string = unicode(string)
    return typo(string)