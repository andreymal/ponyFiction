#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import ceil

from django.shortcuts import redirect, render

from ponyFiction import settings as settings
from ponyFiction.forms.search import SearchForm
from ponyFiction.models import Story, Chapter
from ponyFiction.utils.misc import pagination_ranges
from ponyFiction.sphinx import SphinxError


def search_main(request):
    if request.method not in ('HEAD', 'OPTIONS', 'GET'):
        return redirect('search')

    if settings.SPHINX_DISABLED:
        return render(request, 'search_disabled.html')

    postform = SearchForm(request.GET)
    return search_action(request, postform)


def search_form(request):
    form = SearchForm()
    data = {'form': form, 'page_title': 'Поиск рассказов'}
    return render(request, 'search.html', data)


def search_action(request, postform):
    if not postform.is_valid():
        data = {'form': postform, 'page_title': 'Поиск рассказов'}
        return render(request, 'search.html', data)

    try:
        page_current = int(request.GET['page']) if request.GET['page'] else 1
    except:
        page_current = 1

    query = postform.cleaned_data['q']
    limit = ((page_current - 1) * settings.SPHINX_CONFIG['limit'], settings.SPHINX_CONFIG['limit'])
    search_type = postform.cleaned_data['type']
    sort_type = postform.cleaned_data['sort']

    data = {'page_title': query.strip() or 'Результаты поиска', 'search_type': search_type}

    if search_type == '0':
        try:
            raw_result, result = Story.bl.search(
                query,
                limit,
                int(sort_type),
                only_published=not request.user.is_authenticated() or not request.user.is_staff,
                character=postform.cleaned_data['char'],
                classifier=postform.cleaned_data['cls'],
                category=postform.cleaned_data['genre'],
                rating_id=postform.cleaned_data['rating'],
                original=postform.cleaned_data['original'],
                finished=postform.cleaned_data['finished'],
                freezed=postform.cleaned_data['freezed'],
                min_words=postform.cleaned_data['min_words'],
                max_words=postform.cleaned_data['max_words']
            )
        except SphinxError as exc:
            data = {'form': postform, 'page_title': 'Поиск рассказов', 'error': 'Кажется, есть синтаксическая ошибка в запросе'}
            if settings.DEBUG or request.user.is_superuser:
                data['error'] += ': ' + str(exc)
            return render(request, 'search.html', data)
        
    else:
        try:
            raw_result, result = Chapter.bl.search(
                query,
                limit,
                only_published=not request.user.is_authenticated() or not request.user.is_staff,
            )
        except SphinxError as exc:
            data = {'form': postform, 'page_title': 'Поиск рассказов', 'error': 'Кажется, есть синтаксическая ошибка в запросе'}
            if settings.DEBUG or request.user.is_superuser:
                data['error'] += ': ' + str(exc)
            return render(request, 'search.html', data)

    num_pages = int(ceil(int(raw_result['total'] or 0) / float(settings.SPHINX_CONFIG['limit'])))
    pagination = pagination_ranges(num_pages=num_pages, page=page_current)

    data['form'] = postform
    data['pagination'] = pagination
    data['total'] = int(raw_result['total_found'])
    data['result'] = result
    return render(request, 'search.html', data)


def search_simple(request, search_type, search_id):
    if settings.SPHINX_DISABLED:
        return render(request, 'search_disabled.html')

    bound_data = {'type': 0, 'sort': 1}
    if search_type == 'character':
        bound_data['char'] = [search_id]
    elif search_type == 'category':
        bound_data['genre'] = [search_id]
    elif search_type == 'classifier':
        bound_data['cls'] = [search_id]
    elif search_type == 'rating':
        bound_data['rating'] = [search_id]
    else:
        return search_form(request)

    postform = SearchForm(bound_data)
    if postform.is_valid():
        return search_action(request, postform)
    else:
        return search_form(request)
