# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

def stream_list(request, **kwargs):
    model = kwargs.pop('model', None)
    stream_type = kwargs.pop('type', None)
    if stream_type == 'comments':
        object_list = model.published.order_by('-date')[0:settings.COMMENTS_COUNT['stream']]
        page_title = 'Лента новых комментариев'
    elif stream_type == 'stories':
        object_list = model.published.filter(draft=False,approved=True).order_by('-date')[0:settings.STORIES_COUNT['stream']]
        page_title = 'Лента новых рассказов'
    elif stream_type == 'chapters':
        object_list = model.published.order_by('-date')[0:settings.CHAPTERS_COUNT['stream']]
        page_title = 'Лента новых глав'
    elif stream_type == 'submits':
        if not request.user.is_staff:
            raise PermissionDenied 
        object_list = model.submitted.order_by('-date')[0:settings.CHAPTERS_COUNT['stream']]
        page_title = 'Лента новых поступлений'
    template_name = 'stream/%s.html' % stream_type
    return render(request, template_name, {'object_list': object_list, 'page_title': page_title})