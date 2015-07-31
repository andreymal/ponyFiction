#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404
from django.conf import settings

from ponyFiction.models import Story, Chapter


class stories(Feed):
    title = 'Новые рассказы — {}'.format(settings.SITE_NAME)
    link = '/new/stories/'
    subtitle = 'Новые главы фанфиков'
    title_template = 'feeds/story_title.html'
    description_template = 'feeds/story_description.html'
    feed_type = Atom1Feed

    def items(self):
        return Story.objects.published.order_by('-date')[:settings.RSS['stories']]

    def item_link(self, item):
        return "/story/%i/" % item.id


class chapters(Feed):
    title = 'Обновления глав — {}'.format(settings.SITE_NAME)
    link = '/new/chapters/'
    subtitle = 'Новые главы рассказов'
    title_template = 'feeds/chapter_title.html'
    description_template = 'feeds/chapter_description.html'
    feed_type = Atom1Feed

    def items(self):
        # без заранее подгруженного текста глав почему-то в 20 раз быстрее
        return (
            Chapter.objects.filter(story__in=Story.objects.published)
            .only('id', 'story_id', 'title', 'date', 'updated', 'order')
            .prefetch_related('story', 'story__authors')
            .order_by('-date').cache()[:settings.RSS['chapters']]
        )

    def item_link(self, item):
        return "/story/%i/chapter/%i/" % (item.story_id, item.order)


class story(Feed):
    title_template = 'feeds/chapter_title.html'
    description_template = 'feeds/chapter_description.html'
    feed_type = Atom1Feed

    def get_object(self, request, story_id):
        return get_object_or_404(Story.objects.published, pk=story_id)

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return '/story/%i/' % obj.id

    def subtitle(self, obj):
        return obj.title

    def items(self, obj):
        return Chapter.objects.prefetch_related('story', 'story__authors').filter(story_id=obj.id).order_by('-order')[:settings.RSS['chapters']]

    def item_link(self, item):
        return "/story/%i/chapter/%i/" % (item.story_id, item.order)
