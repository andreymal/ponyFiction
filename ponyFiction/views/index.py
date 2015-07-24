# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from ponyFiction.models import Story, Category, Chapter, Comment

@csrf_protect
def index(request):
    page_title = 'Главная'
    categories = Category.objects.all()
    stories = Story.objects.published.good.order_by('-date')[0:settings.STORIES_COUNT['main']]
    chapters = Chapter.objects.filter(story__in=Story.objects.published).exclude(order=1).order_by('-date').cache()[0:settings.CHAPTERS_COUNT['main']]
    comments = Comment.objects.filter(story__in=Story.objects.published).order_by('-date').cache()[0:settings.COMMENTS_COUNT['main']]
    data = {
        'categories' : categories,
        'stories' : stories,
        'chapters' : chapters,
        'comments' : comments,
        'page_title' : page_title,
    }
    return render(request, 'index.html', data)
