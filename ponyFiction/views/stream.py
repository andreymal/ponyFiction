from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def stream_list(request, **kwargs):
    model = kwargs.pop('model', None)
    page_title = kwargs.pop('page_title', None)
    model_name = model.__name__.lower()
    template_name = 'stream/%s.html' % model_name
    if model_name == 'comment':
        object_list = model.objects.order_by('-date')[0:settings.COMMENTS_COUNT['stream']]
    elif model_name == 'story':
        object_list = model.published.order_by('-date')[0:settings.STORIES_COUNT['stream']]
        return render(request, template_name, {'stories': object_list, 'page_title': page_title})
    elif model_name == 'chapter':
        object_list = model.objects.order_by('-date')[0:settings.CHAPTERS_COUNT['stream']]
    return render(request, template_name, {'object_list': object_list, 'page_title': page_title})