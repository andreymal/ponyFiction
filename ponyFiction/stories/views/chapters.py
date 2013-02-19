# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from ponyFiction.stories.models import Story, Chapter, StoryView
from ponyFiction.stories.forms.chapter import ChapterForm
from django.db.models import F, Max
from django.core.exceptions import PermissionDenied

def chapter_view(request, story_id=False, chapter_order=False):
    if chapter_order:
        story = get_object_or_404(Story, pk=story_id)
        chapter = get_object_or_404(story.chapter_set, order=chapter_order)
        page_title = chapter.title[0:80]+' : '+chapter.in_story.title
        prev_chapter = chapter.get_prev_chapter()
        next_chapter = chapter.get_next_chapter()
        data = {
           'story': story,
           'chapter' : chapter,
           'prev_chapter' : prev_chapter,
           'next_chapter' : next_chapter,
           'page_title' : page_title,
           'allchapters': False
        }
        if request.user.is_authenticated():
            StoryView.objects.create(
                author = request.user,
                story_id = story_id,
                chapter = chapter,
            )
    else:
        story = get_object_or_404(Story, pk=story_id)
        chapters = story.chapter_set.order_by('order')
        page_title = story.title+u' – все главы'
        data = {
            'story': story,
            'chapters' : chapters,
            'page_title' : page_title,
            'allchapters': True
        }
        if request.user.is_authenticated():
            StoryView.objects.create(
                author = request.user,
                story_id = story_id,
            )
    return render(request, 'chapter_view.html', data) 
    

@login_required
@csrf_protect
def chapter_work(request, story_id=False, chapter_id=False):
    # Если передан id рассказа и такой рассказ есть
    story = get_object_or_404(Story, pk=story_id)
    if story.is_editable_by(request.user):
        # Работаем с главами
        if (chapter_id and Chapter.objects.filter(in_story=story_id, id=chapter_id).exists()):
            # Редактируем главу
            return chapter_edit(request, story_id, chapter_id)
        else:
            # Иначе добавляем ее
            return chapter_add(request, story_id)
    # Иначе - на главную
    raise PermissionDenied

def chapter_add(request, story_id):
    data = {}
    story = Story.objects.get(pk=story_id)
    if request.POST:
        # Создание новой главы рассказа на основании данных формы
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.in_story = story
            chapter.order = (story.chapter_set.aggregate(o=Max('order'))['o'] or 0) + 1
            chapter.save()
            # Перенаправление на страницу редактирования в случае успеха
            return redirect('chapter_edit', story.id, chapter.id)
    else:
        # Отправка пустой формы для добавления рассказа.
        form = ChapterForm()
        data['page_title'] = 'Добавить новую главу'
        form.fields['button_submit'].initial = 'Добавить'
    """
    К данным шаблона добавляем форму
    Пустую - в случае новой главы
    Предварительно заполненную неправильно - в случае ошибки при добавлении
    """
    data['form'] = form
    data['story'] = story
    return render(request, 'chapter_work.html', data)

def chapter_edit(request, story_id, chapter_id):
    data={}
    story = Story.objects.get(pk=story_id)
    chapter = Chapter.objects.get(in_story=story_id, id=chapter_id)
    if request.POST:
        if 'button_submit' in request.POST:
            # Редактирование существующей главы рассказа
            form = ChapterForm(request.POST, instance=chapter)
            if form.is_valid():
                chapter = form.save()
        if 'button_delete' in request.POST:
            story.chapter_set.filter(order__gt=chapter.order).update(order=F('order')-1)
            chapter.delete()
            return redirect('story_edit', story_id)
    else:
        # Отправка предварительно заполненной формы с главой
        form = ChapterForm(instance=chapter)
    """
    К данным шаблона добавляем форму
    Предварительно заполненную - в случае успешного редактирования или начальной отправки
    """
    form.fields['button_submit'].initial = 'Сохранить изменения'
    data.update(
        form = form,
        chapter_edit = True,
        page_title = u'Редактирование «%s»' % chapter.title,
        story = story,
        chapter = chapter,
    )
    return render(request, 'chapter_work.html', data)
