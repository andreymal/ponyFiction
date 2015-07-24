# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter
def story_comments_delta(story, author):
    return story.comment_set.count() - story.last_comments_by_author(author)
