#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

from ponyFiction.models import Story, Chapter
from ponyFiction.apis.amsphinxql import SphinxPool, SphinxError


sort_types = {
    0: "weight() DESC, id DESC",
    1: "id DESC",
    2: "size DESC",
    3: "id ASC",  # TODO: rating DESC
    4: "comments DESC"
}


def add_stories(stories):
    stories = [{
        'id': story.id,
        'title': story.title,
        'summary': story.summary,
        'notes': story.notes,
        'rating_id': story.rating_id,
        'size': story.words,
        'comments': story.comment_set.count(),
        'finished': story.finished,
        'original': story.original,
        'freezed': story.freezed,
        'published': story.published,
        'character': story.characters.all(),
        'category': story.categories.all(),
        'classifier': story.classifications.all(),
        'match_author': ' '.join(x.username for x in story.authors.all()),
        'author': story.authors.all()
    } for story in stories]

    return sphinx.add('stories', stories)


def add_chapters(chapters):
    chapters = [{
        'id': chapter.id,
        'title': chapter.title,
        'notes': chapter.notes,
        'text': chapter.text,
        'story_id': chapter.story.id,
        'published': chapter.story.published
    } for chapter in chapters]

    return sphinx.add('chapters', chapters)


def search_stories(query, limit, sort_by=0, only_published=True, **filters):
    if sort_by not in sort_types:
        sort_by = 0

    sphinx_filters = {}
    if only_published:
        sphinx_filters['published'] = 1

    for ofilter in ('character', 'classifier', 'category', 'rating_id'):
        if filters.get(ofilter):
            sphinx_filters[ofilter + '__in'] = [x.id for x in filters[ofilter]]

    for ifilter in ('original', 'finished', 'freezed'):
        if filters.get(ifilter):
            sphinx_filters[ifilter + '__in'] = [int(x) for x in filters[ifilter]]

    if filters.get('min_words') is not None:
        sphinx_filters['size__gte'] = int(filters['min_words'])

    if filters.get('max_words') is not None:
        sphinx_filters['size_lte'] = int(filters['max_words'])

    with sphinx:
        raw_result = sphinx.search(
            'stories',
            query,
            weights=settings.SPHINX_CONFIG['weights_stories'],
            options=settings.SPHINX_CONFIG['select_options'],
            limit=limit,
            sort_by=sort_types[sort_by],
            **sphinx_filters
        )

    ids = [x['id'] for x in raw_result['matches']]
    result = {x.id:x for x in Story.objects.prefetch_for_list.filter(id__in=ids)}
    result = [result[i] for i in ids if i in result]

    return raw_result, result


def search_chapters(query, limit, sort_by=0, only_published=True):
    sort_by = 0  # TODO: сортировка и фильтры для глав

    sphinx_filters = {}
    if only_published:
        sphinx_filters['published'] = 1

    with sphinx:
        raw_result = sphinx.search(
            'chapters',
            query,
            weights=settings.SPHINX_CONFIG['weights_chapters'],
            options=settings.SPHINX_CONFIG['select_options'],
            limit=limit,
            sort_by=sort_types[sort_by],
            **sphinx_filters
        )

        ids = [x['id'] for x in raw_result['matches']]
        dresult = {x.id:x for x in Chapter.objects.prefetch_related('story', 'story__authors').filter(id__in=ids)}
        result = []
        for i in ids:
            if i not in dresult:
                continue
            excerpt = sphinx.call_snippets('chapters', dresult[i].text, query, **settings.SPHINX_CONFIG['excerpts_opts'])
            result.append((dresult[i], excerpt[0] if excerpt else ''))

    return raw_result, result


sphinx = SphinxPool(settings.SPHINX_CONFIG['connection_params'])
