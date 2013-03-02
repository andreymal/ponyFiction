# -*- coding: utf-8 -*-
# TODO: Дописать всем моделям get_absolute_url()
from django.contrib.syndication.views import Feed
from ponyFiction.models import Story, Chapter
from django.conf import settings
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import get_object_or_404

class stories_rss(Feed):
    title = 'Новые рассказы - Библиотека EveryPony.ru'
    link = '/new/stories/'
    description = 'Новые главы фанфиков'
    title_template = 'feeds/stories_title.html'
    description_template = 'feeds/stories_description.html'

    def items(self):
        return Story.objects.order_by('-date')[:settings.RSS['stories']]
    
    def item_link(self, item):
        return "/story/%i/" % item.id

class stories_atom(stories_rss):
    feed_type = Atom1Feed
    subtitle = stories_rss.description

class chapters_rss(Feed):
    title = 'Обновления глав - Библиотека EveryPony.ru'
    link = '/new/chapters/'
    description = 'Новые главы рассказов'
    title_template = 'feeds/chapters_title.html'
    description_template = 'feeds/chapters_description.html'

    def items(self):
        return Chapter.objects.order_by('-date')[:settings.RSS['chapters']]
    
    def item_link(self, item):
        return "/story/%i/chapter/%i/" % (item.story_id, item.order)

class chapters_atom(chapters_rss):
    feed_type = Atom1Feed
    subtitle = chapters_rss.description
    
class story_chapters_rss(Feed):
    
    title_template = 'feeds/chapters_title.html'
    description_template = 'feeds/chapters_description.html'
    
    def get_object(self, request, story_id):
        return get_object_or_404(Story, pk=story_id)
    
    def title(self, obj):
        return obj.title
    
    def link(self, obj):
        return '/story/%i/' % obj.id
    
    def description(self, obj):
        return obj.title

    def items(self, obj):
        return Chapter.objects.filter(story_id=obj.id).order_by('-order')[:settings.RSS['chapters']]
    
    def item_link(self, item):
        return "/story/%i/chapter/%i/" % (item.story_id, item.order)

class story_chapters_atom(story_chapters_rss):
    feed_type = Atom1Feed
    subtitle = chapters_rss.description