# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ponyFiction.models import Author
from ponyFiction.views.stories_list import StoriesList

class FavoritesList(StoriesList):
    
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(FavoritesList, self).dispatch(request, *args, **kwargs)
    
    @property
    def author(self):
        return get_object_or_404(Author, pk=self.kwargs['user_id'])
    
    @property
    def page_title(self):
        if self.author.id == self.request.user.id:
            return u'Мое избранное'
        else:
            return u'Избранное автора %s' % self.author.username

    def get_queryset(self):
        return self.author.favorites_story_set.filter(draft=False, approved=True).order_by('-favorites_set__date')