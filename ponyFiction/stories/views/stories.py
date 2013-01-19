# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from ponyFiction.stories.models import Story, CoAuthorsStory, Chapter
from django.core.paginator import Paginator
from ponyFiction.forms import StoryAddComment, StoryAdd
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

@csrf_protect
def story_view(request, **kwargs):
    story_id = kwargs.pop('story_id', None)
    story = get_object_or_404(Story, pk=story_id)
    chapters = story.chapter_set.order_by('order')
    comments_list = story.comment_set.all()
    paged = Paginator(comments_list, settings.COMMENTS_COUNT['page'], orphans=settings.COMMENTS_ORPHANS)
    num_pages = paged.num_pages
    comments = paged.page(1).object_list
    page_title = story.title
    comment_form = StoryAddComment()
    data = {
       'story' : story,
       'comments' : comments,
       'chapters' : chapters,
       'num_pages' : num_pages,
       'page_title' : page_title,
       'comment_form': comment_form
       }
    return render(request, 'story_view.html', data)

@login_required
@csrf_protect
# TODO: переработать на логику по типу поиска
def story_work(request, **kwargs):
    story_id = kwargs.pop('story_id', False)
    data={}
    # Если передан id истории и такая история есть
    if (story_id and Story.objects.filter(pk=story_id).exists()):
        story = Story.objects.get(pk=story_id)
        # Если пользователь входит в число соавторов
        if (story.authors.filter(id=request.user.id)):
            # Редактирование существующего рассказа
            return story_edit(request, story_id, data)
    # Создание нового рассказа на основании данных формы
    return story_add(request, data)

def story_add(request, data):
    if request.POST:
        # Создание нового рассказа на основании данных формы
        form = StoryAdd(request.POST)
        if form.is_valid():
            story = form.save()
            coauthors = CoAuthorsStory.objects.create()
            coauthors.story = story
            coauthors.author = request.user
            coauthors.approved = True
            coauthors.save()
            # Перенаправление на страницу редактирования в случае успеха
            return HttpResponseRedirect(reverse('story_edit', kwargs={'story_id': story.id}))
    else:
        # Отправка пустой формы для добавления рассказа.
        form = StoryAdd(initial={'freezed': 0, 'original': 1, 'rating': 4, 'size': 1})
        data.update({'page_title' : 'Новый рассказ'})
        form.fields['button_submit'].initial = 'Добавить рассказ'
    """
    К данным шаблона добавляем форму
    Пустую - в случае нового рассказа
    Предварительно заполненную неправильно - в случае ошибки при добавлении
    """
    data.update({'form' : form})
    return render(request, 'story_work.html', data)

def story_edit(request, story_id, data):
    story = Story.objects.get(pk=story_id)
    if request.POST:
        if 'button_submit' in request.POST:
            # Редактирование существующего рассказа
            form = StoryAdd(request.POST, instance=story)
            if form.is_valid():
                form.save()
                data.update({'edit_success': True})
                form = StoryAdd(instance=story)
        if 'button_delete' in request.POST:
            story.delete()
            return HttpResponseRedirect(reverse('author_dashboard'))
    else:
        # Отправка предварительно заполненной формы с рассказом
        form = StoryAdd(instance=story)
    """
    К данным шаблона добавляем форму
    Предварительно заполненную - в случае успешного редактирования или начальной отправки
    """
    form.fields['button_submit'].initial = 'Сохранить изменения'
    chapters = Chapter.objects.filter(in_story=story.id).order_by('order')
    data.update({'form': form, 'story_edit': True, 'chapters': chapters, 'page_title' : 'Редактирование «%s»' % story.title })
    return render(request, 'story_work.html', data)