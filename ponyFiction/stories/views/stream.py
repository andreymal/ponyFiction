# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render

def stream_list(request, **kwargs):
    model = kwargs.pop('model', None)
    if model.__name__.lower() == 'comment':
        object_list = model.objects.order_by('-date')[0:settings.COMMENTS_COUNT['stream']]
        page_title =  'Лента новых комментариев'
    elif model.__name__.lower() == 'story':
        object_list = model.objects.order_by('-date')[0:settings.STORIES_COUNT['stream']]
        page_title =  'Лента новых рассказов'
    elif model.__name__.lower() == 'chapter':
        object_list = model.objects.order_by('-date')[0:settings.CHAPTERS_COUNT['stream']]
        page_title =  'Лента новых глав'
    template_name = 'stream/%s.html' % model.__name__.lower()
    return render(request, template_name, {'object_list': object_list, 'page_title': page_title})