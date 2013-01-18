# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import Http404

@csrf_protect
def chapter_view(request, **kwargs):
    random_stories = kwargs.pop('random_stories', {})
    story_id = kwargs.pop('story_id', None)
    view_type = kwargs.pop('view_type', 'all')
    if view_type == 'single':
        from ponyFiction.stories.models import Chapter
        chapter_id = kwargs.pop('chapter_id', None)
        chapter = get_object_or_404(Chapter, in_story_id=story_id, order=chapter_id)
        page_title = chapter.title[0:80]+' &mdash; '+chapter.in_story.title
        allchapters = False
        if (chapter.in_story.chapter_set.count() > 1):
            prev_id = chapter.order-1
            next_id = chapter.order+1
            try:
                prev_chapter = get_object_or_404(Chapter, in_story_id=story_id, order=prev_id)
            except Http404:
                prev_chapter = False
            try:
                next_chapter = get_object_or_404(Chapter, in_story_id=story_id, order=next_id)
            except Http404:
                next_chapter = False
        else:
            prev_chapter = next_chapter = False
        data = {
           'chapter' : chapter,
           'prev_chapter' : prev_chapter,
           'next_chapter' : next_chapter,
           }
    else:
        from ponyFiction.stories.models import Story
        story = get_object_or_404(Story, pk=story_id)
        chapters = story.chapter_set.all()
        page_title = story.title+u' &mdash; все главы'
        allchapters = True
        data = {
           'chapters' : chapters,
           }
    data.update({'random_stories' : random_stories, 'page_title' : page_title, 'allchapters': allchapters})
    return render(request, 'chapter.html', data)