#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template

from ponyFiction.models import Story


register = template.Library()


@register.inclusion_tag('includes/stories_random.html')
def random_stories():
    stories = Story.bl.get_random()
    return {'random_stories': stories}
