# -*- coding: utf-8 -*-
from django.conf import settings
from ponyFiction.views.object_lists import ObjectList
from ponyFiction.models import Story, Chapter, Comment
from cacheops.query import cached_as

class StreamStories(ObjectList):
    
    paginate_by = settings.STORIES_COUNT['stream']
    template_name = 'stream/stories.html'
    page_title = u'Лента добавлений'

    def get_queryset(self):
        return Story.objects.published.order_by('-date')

class StreamChapters(ObjectList):

    context_object_name = 'chapters'
    paginate_by = settings.CHAPTERS_COUNT['stream']
    template_name = 'stream/chapters.html'
    page_title = u'Лента обновлений'

    def get_queryset(self):
        return Chapter.objects.filter(story__in=Story.objects.published).order_by('-date').cache()

class StreamComments(ObjectList):

    context_object_name = 'comments'
    paginate_by = settings.COMMENTS_COUNT['stream']
    template_name = 'stream/comments.html'
    page_title = u'Лента комментариев'
    
    def get_queryset(self):
        return Comment.objects.filter(story__in=Story.objects.published).order_by('-date').cache()