# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from django.conf import settings

class StoriesList(ListView):
    context_object_name = 'stories'
    template_name = 'stories_list.html'
    paginate_by = settings.STORIES_COUNT['page']

    @property
    def page_title(self):
        raise NotImplementedError("Subclasses should implement this!") 

    def get_queryset(self):
        raise NotImplementedError("Subclasses should implement this!")
        
    def get_context_data(self, **kwargs):
        context = super(StoriesList, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context