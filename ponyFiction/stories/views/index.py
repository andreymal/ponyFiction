# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from ponyFiction.stories.models import Story, Category, Chapter, Comment

@csrf_protect
def index(request, **kwargs):
    random_stories = kwargs.pop('random_stories', {})
    page_title = kwargs.pop('page_title', 'Библиотека')
    categories = Category.objects.all()
    stories = Story.objects.order_by('-date')[0:settings.STORIES_COUNT['main']]
    chapters = Chapter.objects.exclude(order=1).order_by('-date')[0:settings.CHAPTERS_COUNT['main']]
    comments = Comment.objects.order_by('-date')[0:settings.COMMENTS_COUNT['main']]
    data = {
            'categories' : categories,
            'stories' : stories,
            'chapters' : chapters,
            'comments' : comments,
            'random_stories' : random_stories,
            'page_title' : page_title
            }
    return render(request, 'index.html', data)