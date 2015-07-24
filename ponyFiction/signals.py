#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import Sum
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import Signal, receiver

from ponyFiction.models import Chapter, Story, Author, Activity, StoryView, Vote, Comment


story_visited = Signal(providing_args=['story'])
story_viewed = Signal(providing_args=['story', 'chapter'])


@receiver(pre_save, sender=Chapter)
def update_chapter_word_count(sender, instance, **kw):
    from django.template import defaultfilters as filters
    instance.words = filters.wordcount(filters.striptags(instance.text))


@receiver(post_save, sender=Chapter)
def update_story_word_count(sender, instance, **kw):
    instance.story.words = instance.story.chapter_set.aggregate(Sum('words'))['words__sum'] or 0
    instance.story.save(update_fields=['words'])


@receiver(post_delete, sender=Chapter)
def update_story_word_count_deleted(sender, instance, **kw):
    instance.story.words = instance.story.chapter_set.aggregate(Sum('words'))['words__sum'] or 0
    instance.story.save(update_fields=['words'])


@receiver(post_save, sender=Chapter)
def update_story_update_time(sender, instance, **kw):
    story = Story.objects.get(id=instance.story_id)
    story.save(update_fields=['updated'])


@receiver(story_visited, sender=Author)
def story_activity_save(sender, instance, **kwargs):
    if not instance.is_authenticated():
        return
    story = kwargs['story']
    comments_count = kwargs['comments_count']
    activity = Activity.objects.get_or_create(author_id=instance.id, story=story)[0]
    activity.last_views = story.views
    activity.last_comments = comments_count
    activity.last_vote_average = story.vote_average
    activity.last_vote_stddev = story.vote_stddev
    activity.save()


@receiver(story_viewed, sender=Author)
def story_views_save(sender, instance, **kwargs):
    if not instance.is_authenticated():
        return
    story = kwargs['story']
    chapter = kwargs['chapter']
    view = StoryView.objects.create()
    view.author = instance
    view.story_id = story.id
    view.chapter = chapter
    view.save()


@receiver(post_save, sender=Vote)
def votes_update(sender, instance, rating_only=False, **kwargs):
    instance.story.update_rating(rating_only=rating_only)
