# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from ponyFiction.models import Story, Chapter
from ponyFiction.forms.search import SearchForm
from ponyFiction import settings as settings
from ponyFiction.apis.sphinxapi import SphinxClient, SPH_SORT_EXTENDED
from ponyFiction.utils.misc import pagination_ranges, SetBoolSphinxFilter, SetObjSphinxFilter
from django.shortcuts import redirect

def search_main(request):
    if request.method == 'GET':
        return search_form(request)
    elif request.method == 'POST':
        # Создаваем форму с данных POST
        postform = SearchForm(request.POST)
        return search_action(request, postform)
    else:
        raise Http404

@csrf_protect
def search_form(request):
    form = SearchForm()
    data = {'form': form, 'page_title': 'Поиск рассказов'}
    return render(request, 'search.html', data)

@csrf_protect
def search_action(request, postform):
    from math import ceil
    data = {'page_title': 'Результаты поиска'}
    # Новый словарь данных для иницаализации формы
    initial_data = {}
    # Список текстовых сниппетов
    excerpts = []
    # Список результата поиска глав
    chapters = []
    # Если форма правильная, работаем дальше, если нет, отображаем снова.
    if postform.is_valid():
        search_type =  postform.cleaned_data['search_type']
        data['search_type'] = search_type
        initial_data['search_type'] = int(search_type)
    else:
        return redirect('search')
    # Текущая страница поиска
    try:
        page_current = int(request.POST['page_current']) if request.POST['page_current'] else 1
    except:
        page_current = 1
    # Смещение поиска
    offset = (page_current - 1) * settings.SPHINX_CONFIG['number']
    # Настройка параметров сервера
    sphinx = SphinxClient()
    sphinx.SetServer(settings.SPHINX_CONFIG['server'])
    sphinx.SetRetries(settings.SPHINX_CONFIG['retries_count'], settings.SPHINX_CONFIG['retries_delay'])
    sphinx.SetConnectTimeout(float(settings.SPHINX_CONFIG['timeout']))
    sphinx.SetMatchMode(settings.SPHINX_CONFIG['match_mode'])
    sphinx.SetRankingMode(settings.SPHINX_CONFIG['rank_mode'])
    # Лимиты поиска
    sphinx.SetLimits(offset, settings.SPHINX_CONFIG['number'], settings.SPHINX_CONFIG['max'], settings.SPHINX_CONFIG['cutoff'])
    sphinx.SetSelect('id')
    # TODO: Сортировка, yay!
    sphinx.SetSortMode(SPH_SORT_EXTENDED, '@weight DESC, @id DESC')
    # Словарь результатов 
    result = []
    initial_data['search_query'] = postform.cleaned_data['search_query']
    if search_type == '0':
        # Установка весов для полей рассказов   
        sphinx.SetFieldWeights(settings.SPHINX_CONFIG['weights_stories'])
        # Фильтрация
        initial_data.update(SetObjSphinxFilter(sphinx, 'category_id', 'categories_select', postform))
        initial_data.update(SetObjSphinxFilter(sphinx, 'classifier_id', 'classifications_select', postform))
        initial_data.update(SetObjSphinxFilter(sphinx, 'character_id', 'characters_select', postform))
        initial_data.update(SetObjSphinxFilter(sphinx, 'rating_id', 'ratings_select', postform))
        initial_data.update(SetObjSphinxFilter(sphinx, 'size_id', 'sizes_select', postform))
        initial_data.update(SetBoolSphinxFilter(sphinx, 'original', 'originals_select', postform))
        initial_data.update(SetBoolSphinxFilter(sphinx, 'finished', 'finished_select', postform))
        initial_data.update(SetBoolSphinxFilter(sphinx, 'freezed', 'freezed_select', postform))
        # Запрос поиска зассказов
        raw_result = sphinx.Query(postform.cleaned_data['search_query'], 'stories')
        # Обработка результатов поиска рассказов
        for res in raw_result['matches']:
            try:
                story = Story.objects.get(pk=res['id'])
            except Story.DoesNotExist:
                pass
            else:
                result.append(story)
    else:
        # Установка весов для полей глав  
        sphinx.SetFieldWeights(settings.SPHINX_CONFIG['weights_chapters'])
        # Запрос поиска глав
        raw_result = sphinx.Query(postform.cleaned_data['search_query'], 'chapters')
        # Обработка результатов поиска глав и постройка сниппетов текста
        for res in raw_result['matches']:
            try:
                chapter = Chapter.objects.get(pk=res['id'])
            except Chapter.DoesNotExist:
                pass
            else:
                text=[]
                text.append(chapter.text)
                excerpt = sphinx.BuildExcerpts(text, 'chapters', postform.cleaned_data['search_query'], settings.SPHINX_CONFIG['excerpts_opts'])
                excerpts.append(excerpt[0])
                chapters.append(chapter)
        result = zip(chapters, excerpts)
    # Пагинация
    pagination = pagination_ranges(num_pages=int(ceil(raw_result['total']/10.0)), page=page_current)
    # Создаем форму для рендера с данными поиска
    data['form'] = SearchForm(initial=initial_data)
    # Добавляем данные
    data['pagination'] = pagination
    data['total'] = raw_result['total']
    data['result'] = result
    # Закрываем за собой сокет
    sphinx.Close()
    return render(request, 'search.html', data)
  
def search_simple(request, search_type, search_id):
    if search_type == 'character':
        bound_data={'characters_select': [search_id], 'search_type': 0}
    elif search_type == 'category':
        bound_data={'categories_select': [search_id], 'search_type': 0}
    elif search_type == 'classifier':
        bound_data={'classifications_select': [search_id], 'search_type': 0}
    elif search_type == 'rating':
        bound_data={'ratings_select': [search_id], 'search_type': 0}
    elif search_type == 'size':
        bound_data={'sizes_select': [search_id], 'search_type': 0}
    else:
        return search_form(request)
    postform = SearchForm(bound_data)
    if postform.is_valid():
        return search_action(request, postform)
    else:
        return search_form(request)