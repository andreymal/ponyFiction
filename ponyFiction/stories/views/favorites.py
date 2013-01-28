# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render, redirect
from ponyFiction.stories.models import Author
from django.contrib.auth.decorators import login_required

@login_required
def favorites_view(request, user_id):
    if not Author.objects.filter(id=1).exists():
        return redirect('index')
    else:
        author = Author.objects.get(id=user_id)
        #stories = author.favorites_story_set.order_by('-favorites_set__date')[0:settings.STORIES_COUNT['stream']]
        stories={}
        if author.id == request.user.id:
            page_title = 'Мое избранное'
        else:
            page_title = 'Избранное автора %s' % author.username
    return render(request, 'favorites.html', {'stories': stories, 'page_title': page_title})