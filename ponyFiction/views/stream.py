# -*- coding: utf-8 -*-
from django.conf import settings
from ponyFiction.views.object_lists import ObjectList
from ponyFiction.models import Story, Chapter, Comment

class StreamStories(ObjectList):
    
    paginate_by = settings.STORIES_COUNT['stream']
    
    @property
    def template_name(self):
        return 'stream/stories.html'
    
    @property
    def page_title(self):
        return u'Лента добавлений'
    
    def get_queryset(self):
        return Story.objects.published.order_by('-date').cache()
    
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
        return Chapter.objects.filter(story__in=Story.objects.published).order_by('-date').cache()
    
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
        return Comment.objects.filter(story__in=Story.objects.published).order_by('-date').cache()