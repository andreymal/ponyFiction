# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ponyFiction.models import Author
from ponyFiction.utils.misc import pagination_ranges
from django.http.response import Http404

@login_required
def favorites_view(request, user_id, page_id):
    author = get_object_or_404(Author, pk=user_id)
    pagination={'current': int(page_id)}
    # Не изящный путь, дублирование фуункционала PublishedManager
    stories_list = author.favorites_story_set.filter(draft=False, approved=True).order_by('-favorites_set__date')
    stories_paged = Paginator(stories_list, settings.STORIES_COUNT['page'], orphans=settings.COMMENTS_ORPHANS)
    try:
        stories_page = stories_paged.page(page_id)
    except EmptyPage:
        return Http404
    # Пагинация
    (
     pagination['head_range'],
     pagination['head_dots'],
     pagination['locality_range'],
     pagination['tail_dots'],
     pagination['tail_range'],
    ) = pagination_ranges(num_pages=stories_paged.num_pages, page=page_id)
    if author.id == request.user.id:
        page_title = 'Мое избранное'
    else:
        page_title = u'Избранное автора %s' % author.username
    return render(request, 'favorites.html', {'stories': stories_page, 'page_title': page_title, 'pagination': pagination})