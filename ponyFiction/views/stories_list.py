# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.urlresolvers import reverse
from ponyFiction.models import Author, Story

class StoriesList(ListView):
    
    context_object_name = 'stories'
    template_name = 'stories_list.html'
    paginate_by = settings.STORIES_COUNT['page']

    @property
    def page_title(self):
        raise NotImplementedError("Subclasses should implement this!") 

    @property
    def page_url(self):
        raise NotImplementedError("Subclasses should implement this!") 
    
    def get_queryset(self):
        raise NotImplementedError("Subclasses should implement this!")
        
    def get_context_data(self, **kwargs):
        context = super(StoriesList, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['page_url'] = self.page_url
        return context

class FavoritesList(StoriesList):
    
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(FavoritesList, self).dispatch(request, *args, **kwargs)
    
    @property
    def author(self):
        return get_object_or_404(Author, pk=self.kwargs['user_id'])
    
    @property
    def page_url(self):
        return reverse('favorites', args=(self.kwargs['user_id'],))
    
    @property
    def page_title(self):
        if self.author.id == self.request.user.id:
            return u'Мое избранное'
        else:
            return u'Избранное автора %s' % self.author.username

    def get_queryset(self):
        return self.author.favorites_story_set.filter(draft=False, approved=True).order_by('-favorites_set__date')
    

class SubmitsList(StoriesList):
    
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(SubmitsList, self).dispatch(request, *args, **kwargs)

    @property
    def page_title(self):
        return u'Новые поступления'
    
    @property
    def page_url(self):
        return reverse('submitted')
    
    def get_queryset(self):
        return Story.submitted.all()
