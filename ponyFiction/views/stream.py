# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import PermissionDenied

from ponyFiction.views.object_lists import ObjectList
from ponyFiction.models import Story, Chapter, Comment, StoryEditLogItem


class StreamStories(ObjectList):
    paginate_by = settings.STORIES_COUNT['stream']
    template_name = 'stream/stories.html'
    page_title = 'Лента добавлений'
    view_name = 'stream_stories_page'

    def get_queryset(self):
        return Story.objects.published.order_by('-date').prefetch_for_list


class TopStories(StreamStories):
    page_title = 'Топ рассказов'
    view_name = 'top_stories'

    def get_queryset(self):
        return Story.objects.published.filter(vote_total__gt=settings.STARS_MINIMUM_VOTES).order_by('-vote_average')


class StreamChapters(ObjectList):
    context_object_name = 'chapters'
    paginate_by = settings.CHAPTERS_COUNT['stream']
    template_name = 'stream/chapters.html'
    page_title = 'Лента обновлений'

    def get_queryset(self):
        return Chapter.objects.filter(story__in=Story.objects.published).order_by('-date').cache()


class StreamComments(ObjectList):
    context_object_name = 'comments'
    paginate_by = settings.COMMENTS_COUNT['stream']
    template_name = 'stream/comments.html'
    page_title = 'Лента комментариев'

    def get_queryset(self):
        return Comment.objects.filter(story__in=Story.objects.published).order_by('-date').cache()


class StreamStoryEditLog(ObjectList):
    context_object_name = 'edit_log'
    paginate_by = getattr(settings, 'EDIT_LOGS_PER_PAGE', 100)
    template_name = 'story_edit_log.html'
    page_title = 'Лог модерации'
    view_name = 'stream_edit_log'

    def get_queryset(self):
        if self.request.user.is_staff:
            return StoryEditLogItem.objects.filter(is_staff=True).order_by('date').select_related()
        else:
            raise PermissionDenied
