# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from ponyFiction.models import Author
from django.contrib.auth.decorators import login_required

@login_required
def favorites_view(request, user_id, page_id=1):
    author = get_object_or_404(Author, pk=user_id)
    stories={}
    if author.id == request.user.id:
        page_title = 'Мое избранное'
    else:
        page_title = u'Избранное автора %s' % author.username
    return render(request, 'favorites.html', {'stories': stories, 'page_title': page_title})