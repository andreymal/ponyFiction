# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter
def favorited(story, author):
    return bool(story.favorites_story_related_set.filter(author=author))

@register.filter
def bookmarked(story, author):
    return bool(story.bookmarks_related_set.filter(author=author))

@register.filter
def chapter_readed(chapter, author):
    return bool(chapter.chapter_views_set.filter(author=author))

@register.filter
def editable_by(story, author):
    return story.editable_by(author)

@register.filter
def deletable_by(story, user):
    return story.deletable_by(user)

@register.filter
def order_by(queryset, order):
    return queryset.order_by(order)