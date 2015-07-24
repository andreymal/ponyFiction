#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery import shared_task
from django.conf import settings

from .models import Story, Chapter
from .sphinx import sphinx, add_stories, add_chapters


@shared_task
def sphinx_update_story(story_id, update_fields):
    if settings.SPHINX_DISABLED:
        print('disabled')
        return
    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        return

    f = set(update_fields)
    if f and not f - {'vote_average', 'vote_stddev', 'vote_total'}:
        pass  # TODO: рейтинг
    elif f and not f - {'date', 'draft', 'approved'}:
        with sphinx:
            sphinx.update('stories', fields={'published': int(story.published)}, id=story_id)
            sphinx.update('chapters', fields={'published': int(story.published)}, id__in=[x.id for x in story.chapter_set.only('id')])
    else:
        with sphinx:
            add_stories((story,))


@shared_task
def sphinx_update_chapter(chapter_id):
    if settings.SPHINX_DISABLED:
        return
    try:
        chapter = Chapter.objects.get(pk=chapter_id)
    except Chapter.DoesNotExist:
        return

    with sphinx:
        add_chapters((chapter,))
        sphinx.update('stories', fields={'size': int(chapter.story.words)}, id=chapter.story_id)


@shared_task
def sphinx_update_comments_count(story_id):
    if settings.SPHINX_DISABLED:
        return
    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        return

    with sphinx:
        sphinx.update('stories', fields={'comments': int(story.comment_set.count())}, id=story_id)


@shared_task
def sphinx_delete_story(story_id):
    if settings.SPHINX_DISABLED:
        return
    try:
        with sphinx:
            sphinx.delete('stories', id=story_id)
        with sphinx:
            sphinx.delete('chapters', story_id=story_id)
    except:
        import traceback
        print(traceback.format_exc())


@shared_task
def sphinx_delete_chapter(story_id, chapter_id):
    if settings.SPHINX_DISABLED:
        return
    with sphinx:
        sphinx.delete('chapters', id=chapter_id)

    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        return

    with sphinx:
        sphinx.update('stories', fields={'size': int(story.words)}, id=story_id)
