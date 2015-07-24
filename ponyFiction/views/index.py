# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from ponyFiction.models import Story, Category, Chapter, Comment

@csrf_protect
def index(request):
    page_title = 'Главная'
    categories = Category.objects.all()

    stories = (
        Story.objects.prefetch_for_list.published.good.order_by('-date')[0:settings.STORIES_COUNT['main']]
    )

    chapters = (
        Chapter.objects.filter(story__in=Story.objects.published).exclude(order=1).order_by('-date', '-id')
        .only('id', 'story_id', 'title', 'date', 'updated', 'order')
        .cache()[0:settings.CHAPTERS_COUNT['main']]
    )
    # так намного быстрее
    story_ids = [y.story_id for y in chapters]
    chapters_stories = {x.id:x for x in Story.objects.filter(id__in=story_ids).prefetch_related('authors')}
    chapters = [(x, chapters_stories[x.story_id]) for x in chapters]

    comments = (
        Comment.objects.filter(story__in=Story.objects.published).order_by('-date')
        .prefetch_related('author', 'story')
        .cache()[0:settings.COMMENTS_COUNT['main']]
    )

    data = {
        'categories' : categories,
        'stories' : stories,
        'chapters' : chapters,
        'comments' : comments,
        'page_title' : page_title,
    }
    return render(request, 'index.html', data)
