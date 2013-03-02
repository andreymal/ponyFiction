from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def stream_list(request, **kwargs):
    model = kwargs.pop('model', None)
    page_title = kwargs.pop('page_title', None)
    if model.__name__.lower() == 'comment':
        object_list = model.objects.order_by('-date')[0:settings.COMMENTS_COUNT['stream']]
    elif model.__name__.lower() == 'story':
        object_list = model.published.order_by('-date')[0:settings.STORIES_COUNT['stream']]
    elif model.__name__.lower() == 'chapter':
        object_list = model.objects.order_by('-date')[0:settings.CHAPTERS_COUNT['stream']]
    template_name = 'stream/%s.html' % model.__name__.lower()
    return render(request, template_name, {'object_list': object_list, 'page_title': page_title})