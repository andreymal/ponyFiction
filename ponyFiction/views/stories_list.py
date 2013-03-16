# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from ponyFiction.models import Author, Story

class StoriesList(ListView):
    
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
        context = super(StoriesList, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

class FavoritesList(StoriesList):
    
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
        return self.author.favorites_story_set.filter(draft=False, approved=True).order_by('-favorites_story_related_set__date')
    

class SubmitsList(StoriesList):
    
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
        return Story.submitted.all()

class DeferredStoriesList(StoriesList):
    
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(DeferredStoriesList, self).dispatch(request, *args, **kwargs)
    
    @property
    def template_name(self):
        return 'favorites.html'

    @property
    def page_title(self):
        return u'Закладки: рассказы'
    
    def get_queryset(self):
        return self.request.user.deferred_story_set.all()