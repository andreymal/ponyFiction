# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from ponyFiction.models import Author, Story


class ObjectList(ListView):
    context_object_name = 'stories'
    paginate_by = settings.STORIES_COUNT['page']
    view_name = None

    @property
    def page_title(self):
        raise NotImplementedError("Subclasses should implement this!")

    @property
    def template_name(self):
        raise NotImplementedError("Subclasses should implement this!")

    def get_queryset(self):
        raise NotImplementedError("Subclasses should implement this!")

    def get_context_data(self, **kwargs):
        context = super(ObjectList, self).get_context_data(**kwargs)
        context.update(
            page_title=self.page_title,
            pagination_view_name=self.view_name,
        )
        return context


class FavoritesList(ObjectList):
    @property
    def author(self):
        return get_object_or_404(Author, pk=self.kwargs['user_id'])

    template_name = 'favorites.html'

    @property
    def page_title(self):
        if self.author.id == self.request.user.id:
            return 'Мое избранное'
        else:
            return 'Избранное автора %s' % self.author.username

    def get_queryset(self):
        return self.author.favorites_story_set.accessible(user=self.request.user).order_by('-favorites_story_related_set__date')

    def get_context_data(self, **kwargs):
        context = ObjectList.get_context_data(self, **kwargs)
        context['author_id'] = self.author.id  # workaround для работы пагинатора в избранном.
        return context


class SubmitsList(ObjectList):
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(SubmitsList, self).dispatch(request, *args, **kwargs)

    template_name = 'submitted.html'
    page_title = 'Новые поступления'

    def get_queryset(self):
        return Story.objects.submitted.prefetch_for_list


class BookmarksList(ObjectList):
    template_name = 'bookmarks.html'
    page_title = 'Закладки'

    def get_queryset(self):
        return self.request.user.bookmarked_story_set.all().cache()
