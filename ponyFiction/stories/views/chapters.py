# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from ponyFiction.stories.models import Story, Chapter
from ponyFiction.forms import ChapterForm

def chapter_view_all(request, story_id=False):
    story = get_object_or_404(Story, pk=story_id)
    chapters = story.chapter_set.order_by('order')
    page_title = story.title+u' – все главы'
    data = {'chapters' : chapters, 'page_title' : page_title, 'allchapters': True}
    return render(request, 'chapter.html', data)

def chapter_view_single(request, story_id=False, chapter_order=False):
    chapter = get_object_or_404(Chapter, in_story_id=story_id, order=chapter_order)
    page_title = chapter.title[0:80]+' – '+chapter.in_story.title
    if (chapter.in_story.chapter_set.count() > 1):
        try:
            prev_chapter = Chapter.objects.get(in_story_id=story_id, order=chapter.order-1)
        except Chapter.DoesNotExist:
            prev_chapter = False
        try:
            next_chapter = Chapter.objects.get(in_story_id=story_id, order=chapter.order+1)
        except Chapter.DoesNotExist:
            next_chapter = False
    else:
        prev_chapter = next_chapter = False
    data = {
       'chapter' : chapter,
       'prev_chapter' : prev_chapter,
       'next_chapter' : next_chapter,
       'page_title' : page_title,
       'allchapters': False
    }
    return render(request, 'chapter.html', data)

@login_required
@csrf_protect
def chapter_work(request, story_id=False, chapter_order=False):
    # Если передан id истории и такая история есть
    if (story_id and Story.objects.filter(pk=story_id).exists()):
        story = Story.objects.get(pk=story_id)
        # Если пользователь входит в число соавторов
        if (story.authors.filter(id=request.user.id)):
            # Работаем с главами
            if (chapter_order and Chapter.objects.filter(in_story=story_id, order=chapter_order).exists()):
                # Редактируем главу
                return chapter_edit(request, story_id, chapter_order)
            else:
                # Иначе добавляем ее
                return chapter_add(request, story_id)
        # Иначе - смотреть историю
        return redirect('story_view', kwargs={'story_id': story.id})
    # Иначе - на главную
    return redirect('index')

def chapter_add(request, story_id):
    data = {}
    story = Story.objects.get(pk=story_id)
    if request.POST:
        # Создание новой главы рассказа на основании данных формы
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.in_story = story
            chapter.order = story.chapter_set.count()+1
            chapter.save()
            # Перенаправление на страницу редактирования в случае успеха
            return redirect('story_edit', kwargs={'story_id': story.id})
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

def chapter_edit(request, story_id, chapter_order):
    data={}
    story = Story.objects.get(pk=story_id)
    chapter = Chapter.objects.get(in_story=story_id, order=chapter_order)
    if request.POST:
        if 'button_submit' in request.POST:
            # Редактирование существующей главы рассказа
            form = ChapterForm(request.POST, instance=chapter)
            if form.is_valid():
                form.save()
                data['edit_success'] = True
                form = ChapterForm(instance=chapter)
        if 'button_delete' in request.POST:
            shift = story.chapter_set.filter(order__gt=chapter.order)
            for chapter in shift:
                chapter.order = chapter.order-1
                chapter.save(update_fields=['order'])
            chapter.delete()
            return redirect('story_edit', kwargs={'story_id': story_id})
    else:
        # Отправка предварительно заполненной формы с главой
        form = ChapterForm(instance=chapter)
    """
    К данным шаблона добавляем форму
    Предварительно заполненную - в случае успешного редактирования или начальной отправки
    """
    form.fields['button_submit'].initial = 'Сохранить изменения'
    data.update({'form': form, 'chapter_edit': True, 'page_title' : 'Редактирование «%s»' % chapter.title, 'story': story })
    return render(request, 'chapter_work.html', data)