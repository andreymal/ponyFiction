# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ponyFiction.models import Author

@login_required
def favorites_view(request, user_id, page_id=1):
    author = get_object_or_404(Author, pk=user_id)
    # Не изящный путь, дублирование фуункционала PublishedManager
    stories = author.favorites_story_set.filter(draft=False, approved=True).order_by('-favorites_set__date')
    if author.id == request.user.id:
        page_title = 'Мое избранное'
    else:
        page_title = u'Избранное автора %s' % author.username
    return render(request, 'favorites.html', {'stories': stories, 'page_title': page_title})