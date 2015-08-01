#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery import shared_task

from .models import Story, Chapter


@shared_task
def sphinx_update_story(story_id, update_fields):
    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        return

    story.bl.search_update(update_fields)


@shared_task
def sphinx_update_chapter(chapter_id):
    try:
        chapter = Chapter.objects.get(pk=chapter_id)
    except Chapter.DoesNotExist:
        return

    chapter.bl.search_add()


@shared_task
def sphinx_update_comments_count(story_id):
    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        return

    story.bl.search_update(('comments',))


@shared_task
def sphinx_delete_story(story_id):
    Story.bl.delete_stories_from_search((story_id,))


@shared_task
def sphinx_delete_chapter(story_id, chapter_id):
    Chapter.bl.delete_chapters_from_search((chapter_id,))

    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        return

    story.bl.search_update(('words',))
