# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from ponyFiction.models import Author, Story

class ObjectList(ListView):
    
    context_object_name = 'stories'
    paginate_by = settings.STORIES_COUNT['page']

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
        context['page_title'] = self.page_title
	context['author_id'] = self.author.id # workaround для работы пагинатора в избранном.
        return context

class FavoritesList(ObjectList):
    
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(FavoritesList, self).dispatch(request, *args, **kwargs)
    
    @property
    def author(self):
        return get_object_or_404(Author, pk=self.kwargs['user_id'])
    
    @property
    def template_name(self):
        return 'favorites.html'
    
    @property
    def page_title(self):
        if self.author.id == self.request.user.id:
            return u'Мое избранное'
        else:
            return u'Избранное автора %s' % self.author.username

    def get_queryset(self):
        return self.author.favorites_story_set.accessible(user=self.request.user).order_by('-favorites_story_related_set__date')
    

class SubmitsList(ObjectList):
    
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(SubmitsList, self).dispatch(request, *args, **kwargs)
    
    @property
    def template_name(self):
        return 'submitted.html'

    @property
    def page_title(self):
        return u'Новые поступления'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Story.objects.submitted
        else:
            return Story.objects.submitted.last_week

class BookmarksList(ObjectList):
    
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(BookmarksList, self).dispatch(request, *args, **kwargs)
    
    @property
    def template_name(self):
        return 'bookmarks.html'

    @property
    def page_title(self):
        return u'Закладки'
    
    def get_queryset(self):
        return self.request.user.bookmarked_story_set.all().cache()
