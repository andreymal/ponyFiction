# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter
def faved(story, author):
    return bool(story.favorites_set.filter(author=author))

@register.filter
def is_editable_by(story, author):
    return story.is_editable_by(author)