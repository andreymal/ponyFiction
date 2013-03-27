# -*- coding: utf-8 -*-
# TODO: Дописать всем моделям get_absolute_url()
from django.contrib.syndication.views import Feed
from ponyFiction.models import Story, Chapter
from django.conf import settings
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404

class stories(Feed):
    title = 'Новые рассказы - Библиотека EveryPony.ru'
    link = '/new/stories/'
    subtitle = 'Новые главы фанфиков'
    title_template = 'feeds/stories_title.html'
    description_template = 'feeds/stories_description.html'
    feed_type = Atom1Feed

    def items(self):
        return Story.objects.published.order_by('-date')[:settings.RSS['stories']]
    
    def item_link(self, item):
        return "/story/%i/" % item.id

class chapters(Feed):
    title = 'Обновления глав - Библиотека EveryPony.ru'
    link = '/new/chapters/'
    subtitle = 'Новые главы рассказов'
    title_template = 'feeds/chapters_title.html'
    description_template = 'feeds/chapters_description.html'
    feed_type = Atom1Feed

    def items(self):
        return Chapter.objects.filter(story__in=Story.objects.published).order_by('-date')[:settings.RSS['chapters']]
    
    def item_link(self, item):
        return "/story/%i/chapter/%i/" % (item.story_id, item.order)

class story(Feed):    
    title_template = 'feeds/chapters_title.html'
    description_template = 'feeds/chapters_description.html'
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
        return Chapter.objects.filter(story_id=obj.id).order_by('-order')[:settings.RSS['chapters']]
    
    def item_link(self, item):
        return "/story/%i/chapter/%i/" % (item.story_id, item.order)