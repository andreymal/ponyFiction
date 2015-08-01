# -*- coding: utf-8 -*-
from django import template
from ponyFiction.utils.typographus import typo
register = template.Library()


@register.filter
def typogrify(string):
    if not isinstance(string, str):
        string = str(string)
    return typo(string)
