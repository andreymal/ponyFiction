# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import Http404, HttpResponseRedirect
from ponyFiction.stories.models import Story, Chapter
from django.core.urlresolvers import reverse

@csrf_protect
def chapter_view(request, **kwargs):
    random_stories = kwargs.pop('random_stories', {})
    story_id = kwargs.pop('story_id', None)
    view_type = kwargs.pop('view_type', 'all')
    if view_type == 'single':
        chapter_order = kwargs.pop('chapter_order', None)
        chapter = get_object_or_404(Chapter, in_story_id=story_id, order=chapter_order)
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
        story = get_object_or_404(Story, pk=story_id)
        chapters = story.chapter_set.all()
        page_title = story.title+u' &mdash; все главы'
        allchapters = True
        data = {
           'chapters' : chapters,
           }
    data.update({'random_stories' : random_stories, 'page_title' : page_title, 'allchapters': allchapters})
    return render(request, 'chapter.html', data)

@login_required
@csrf_protect
def chapter_work(request, **kwargs):
    random_stories = kwargs.pop('random_stories', {})
    story_id = kwargs.pop('story_id', False)
    chapter_order = kwargs.pop('chapter_order', False)
    data={'random_stories': random_stories}
    # Если передан id истории и такая история есть
    if (story_id and Story.objects.filter(pk=story_id).exists()):
        story = Story.objects.get(pk=story_id)
        # Если пользователь входит в число соавторов
        if (story.authors.filter(id=request.user.id)):
            # Редактирование существующего рассказа
            # return story_edit(request, story_id, data)
            pass
        # Иначе - смотреть историю
        return HttpResponseRedirect(reverse('story_view', kwargs={'story_id': story.id}))
    # Иначе - на главную
    return HttpResponseRedirect(reverse('index'))