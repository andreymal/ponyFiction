#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from django.core.cache import cache

from ponyFiction.models import Story
from django import template
register = template.Library()


def get_random_story_ids(count=10):
    # это быстрее, чем RAND() в MySQL
    ids = cache.get('all_story_ids')
    if not ids:
        ids = tuple(Story.objects.published.order_by('date').values_list('id', flat=True))
        cache.set('all_story_ids', ids, 300)
    if len(ids) <= count:
        return ids
    else:
        return random.sample(ids, count)


@register.inclusion_tag('includes/stories_random.html')
def random_stories():
    stories = Story.objects.filter(id__in=get_random_story_ids()).prefetch_related('categories', 'characters')
    return {'random_stories': stories}
