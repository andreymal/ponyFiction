# -*- coding: utf-8 -*-

from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_protect

from ponyFiction.ajax.shortcuts import ajax_response


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def ajax_login_required(f):
    f = csrf_protect(f)

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return ajax_response(request, {'error': 'Это не похоже на AJAX-запрос', 'success': False}, status=400)
        if not request.user.is_authenticated():
            return ajax_response(request, {'error': 'Необходимо авторизоваться!', 'success': False}, status=401)
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
