# -*- coding: utf-8 -*-
from django.conf import settings
from ponyFiction.views.object_lists import ObjectList
from ponyFiction.models import Story, Chapter, Comment
from cacheops.query import cached_as

class StreamStories(ObjectList):
    
    paginate_by = settings.STORIES_COUNT['stream']
    
    @property
    def template_name(self):
        return 'stream/stories.html'
    
    @property
    def page_title(self):
        return u'Лента добавлений'
    
    @cached_as(Story.objects.all()) # workaround for https://github.com/Suor/django-cacheops/issues/29
    def get_queryset(self):
        return Story.objects.accessible(user=self.request.user).order_by('-date')
    
class StreamChapters(ObjectList):
    
    context_object_name = 'chapters'
    paginate_by = settings.CHAPTERS_COUNT['stream']
    
    @property
    def template_name(self):
        return 'stream/chapters.html'
    
    @property
    def page_title(self):
        return u'Лента обновлений'
    
    def get_queryset(self):
        return Chapter.objects.filter(story__in=Story.objects.accessible(user=self.request.user)).order_by('-date').cache()
    
class StreamComments(ObjectList):
    
    context_object_name = 'comments'
    paginate_by = settings.COMMENTS_COUNT['stream']
    
    @property
    def template_name(self):
        return 'stream/comments.html'
    
    @property
    def page_title(self):
        return u'Лента комментариев'
    
    def get_queryset(self):
        return Comment.objects.filter(story__in=Story.objects.accessible(user=self.request.user)).order_by('-date').cache()