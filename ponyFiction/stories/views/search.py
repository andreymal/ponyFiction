# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from ponyFiction.stories.models import Story, Chapter
from ponyFiction.forms import SearchForm

def search_main(request):
    if request.method == 'GET':
        return search_form(request)
    elif request.method == 'POST':
        return search_action(request)
    else:
        raise Http404

@csrf_protect
def search_form(request):
    form = SearchForm()
    data = {'form': form, 'page_title': 'Поиск историй'}
    return render(request, 'search.html', data)

@csrf_protect
def search_action(request):
    from django.conf import settings
    from ponyFiction.stories.apis.sphinxapi import SphinxClient, SPH_SORT_EXTENDED
    from ponyFiction.stories.apis.utils import pagination_ranges, SetBoolSphinxFilter, SetObjSphinxFilter
    from math import ceil
    data = {'page_title': 'Результаты поиска'}
    # Создаваем форму с данных POST
    postform = SearchForm(request.POST)
    # Новый словарь данных для иницаализации формы
    initial_data = {}
    # Словарь результатов 
    result = {'stories': [], 'chapters_data': None }
    # Словарь данных пагинации
    pagination = {'stories': {}, 'chapters': {}}
    # Список текстовых сниппетов
    excerpts = []
    # Список результата поиска глав
    chapters = []
    # Если форма правильная, работаем дальше, если нет, отображаем снова.
    if postform.is_valid():
        pass
    else:
        form = SearchForm()
        data['form'] = form
        return render(request, 'search.html', data)
    # Текущая страница поиска
    try:
        page_current_stories = int(request.POST['page_current_stories']) if request.POST['page_current_stories'] else 1
    except:
        page_current_stories = 1
    try:
        page_current_chapters = int(request.POST['page_current_chapters']) if request.POST['page_current_chapters'] else 1
    except:
        page_current_chapters = 1
    # Активная вкладка
    try:
        active_tab = 'stories' if request.POST['page_current_chapters'] == 'stories' else 'chapters'
    except:
        active_tab = 'stories'  
    # Смещение поиска
    offset_stories = (page_current_stories - 1) * settings.SPHINX_CONFIG['number']
    offset_chapters = (page_current_chapters - 1) * settings.SPHINX_CONFIG['number']
    # Настройка параметров сервера
    sphinx = SphinxClient()
    sphinx.SetServer(settings.SPHINX_CONFIG['server'])
    sphinx.SetRetries(settings.SPHINX_CONFIG['retries_count'], settings.SPHINX_CONFIG['retries_delay'])
    sphinx.SetConnectTimeout(float(settings.SPHINX_CONFIG['timeout']))
    sphinx.SetMatchMode(settings.SPHINX_CONFIG['match_mode'])
    sphinx.SetRankingMode(settings.SPHINX_CONFIG['rank_mode'])
    # Лимиты поиска рассказов
    sphinx.SetLimits(offset_stories, settings.SPHINX_CONFIG['number'], settings.SPHINX_CONFIG['max'], settings.SPHINX_CONFIG['cutoff'])
    # Установка весов для полей рассказов   
    sphinx.SetFieldWeights(settings.SPHINX_CONFIG['weights_stories'])
    sphinx.SetSelect('id')
    # TODO: Сортировка, yay!
    sphinx.SetSortMode(SPH_SORT_EXTENDED, '@weight DESC, @id DESC')
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
    raw_result_stories = sphinx.Query(postform.cleaned_data['search_query'], 'stories')
    initial_data.update({'search_query': postform.cleaned_data['search_query']})
    # Обработка результатов поиска рассказов
    for res in raw_result_stories['matches']:
        result['stories'].append(Story.objects.get(pk=res['id']))
    # Сброс фильтров
    sphinx.ResetFilters()
    # Лимиты поиска глав
    sphinx.SetLimits(offset_chapters, settings.SPHINX_CONFIG['number'], settings.SPHINX_CONFIG['max'], settings.SPHINX_CONFIG['cutoff'])
    # Установка весов для полей глав  
    sphinx.SetFieldWeights(settings.SPHINX_CONFIG['weights_chapters'])
    # Запрос поиска глав
    raw_result_chapters = sphinx.Query(postform.cleaned_data['search_query'], 'chapters')
    # Обработка результатов поиска глав и постройка сниппетов текста
    for res in raw_result_chapters['matches']:
        chapter = Chapter.objects.get(pk=res['id'])
        text=[]
        text.append(chapter.text)
        excerpt = sphinx.BuildExcerpts(text, 'chapters', postform.cleaned_data['search_query'], settings.SPHINX_CONFIG['excerpts_opts'])
        excerpts.append(excerpt[0])
        chapters.append(chapter)
    result['chapters_data'] = zip(chapters, excerpts)
    # Пагинация
    (
     pagination['stories']['head_range'],
     pagination['stories']['head_dots'],
     pagination['stories']['locality_range'],
     pagination['stories']['tail_dots'],
     pagination['stories']['tail_range'],
    ) = pagination_ranges(num_pages=int(ceil(raw_result_stories['total']/10.0)), page=page_current_stories)
    (
     pagination['chapters']['head_range'],
     pagination['chapters']['head_dots'],
     pagination['chapters']['locality_range'],
     pagination['chapters']['tail_dots'],
     pagination['chapters']['tail_range'],
    ) = pagination_ranges(num_pages=int(ceil(raw_result_chapters['total']/10.0)), page=page_current_chapters)
    pagination['stories']['current'] = page_current_stories
    pagination['chapters']['current'] = page_current_chapters
    # Создаем форму для рендера с данными поиска
    newform = SearchForm(initial=initial_data)
    # Добавляем данные 
    data.update({
        'result': result,
        'pagination': pagination, 
        'active_tab' : active_tab,
        'stories_found' : raw_result_stories['total'],
        'chapters_found' : raw_result_chapters['total'],
        'form': newform
        })
    return render(request, 'search.html', data)
        
def search_simple(request, search_type, search_id):
    pass