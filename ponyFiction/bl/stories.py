#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from django.conf import settings

from .utils import BaseBL
from ..sphinx import sphinx


class StoryBL(BaseBL):
    sort_types = {
        0: "weight() DESC, id DESC",
        1: "id DESC",
        2: "size DESC",
        3: "id ASC",  # TODO: rating DESC
        4: "comments DESC"
    }

    def create(self, authors, title, categories, characters, summary, rating, original, freezed, finished, notes=None, classifications=None):
        from ..models import CoAuthorsStory
        from ..tasks import sphinx_update_story

        story = self.model.objects.create(
            title=title,
            summary=summary,
            rating=rating,
            original=original,
            freezed=freezed,
            finished=finished,
            notes=notes or '',
        )
        story.categories.set(categories)
        story.characters.set(characters)
        story.classifications.set(classifications)
        for author, approved in authors:
            CoAuthorsStory.objects.create(story=story, author=author, approved=approved)

        sphinx_update_story.delay(story.id, ())
        return story

    def update(self, editor, **data):
        from ..models import StoryEditLogItem
        from ..tasks import sphinx_update_story

        story = self.model
        for key, value in data.items():
            if key in ('categories', 'characters', 'classifications'):
                getattr(story, key).set(value)
            else:
                setattr(story, key, value)
        story.save()
        if editor:
            StoryEditLogItem.create(
                action=StoryEditLogItem.Actions.Edit,
                user=editor,
                story=story,
                data=data,
            )
        sphinx_update_story.delay(story.id, ())
        return story

    def delete(self):
        self.model.delete()

    def add_stories_to_search(self, stories):
        if settings.SPHINX_DISABLED:
            return
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

        with sphinx:
            sphinx.add('stories', stories)

    def delete_stories_from_search(self, story_ids):
        if settings.SPHINX_DISABLED:
            return
        with sphinx:
            sphinx.delete('stories', id__in=story_ids)
        with sphinx:
            sphinx.delete('chapters', story_id__in=story_ids)

    def search_add(self):
        self.add_stories_to_search((self.model,))

    def search_update(self, update_fields=()):
        if settings.SPHINX_DISABLED:
            return
        story = self.model
        f = set(update_fields)
        if f and not f - {'vote_average', 'vote_stddev', 'vote_total'}:
            pass  # TODO: рейтинг
        elif f and not f - {'date', 'draft', 'approved'}:
            with sphinx:
                sphinx.update('stories', fields={'published': int(story.published)}, id=story.id)
                sphinx.update('chapters', fields={'published': int(story.published)}, id__in=[x.id for x in story.chapter_set.only('id')])
        elif f == {'words'}:
            with sphinx:
                sphinx.update('stories', fields={'size': int(story.words)}, id=story.id)
        elif f == {'comments'}:
            with sphinx:
                sphinx.update('stories', fields={'comments': int(story.comment_set.count())}, id=story.id)
        else:
            with sphinx:
                self.add_stories_to_search((story,))

    def search_delete(self):
        self.delete_stories_from_search((self.model.id,))

    def search(self, query, limit, sort_by=0, only_published=True, **filters):
        if settings.SPHINX_DISABLED:
            return {}, []

        if sort_by not in self.sort_types:
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
            sphinx_filters['size__lte'] = int(filters['max_words'])

        with sphinx:
            raw_result = sphinx.search(
                'stories',
                query,
                weights=settings.SPHINX_CONFIG['weights_stories'],
                options=settings.SPHINX_CONFIG['select_options'],
                limit=limit,
                sort_by=self.sort_types[sort_by],
                **sphinx_filters
            )

        ids = [x['id'] for x in raw_result['matches']]
        result = {x.id: x for x in self.model.objects.prefetch_for_list.filter(id__in=ids)}
        result = [result[i] for i in ids if i in result]

        return raw_result, result

    def get_random(self, count=10):
        from django.core.cache import cache
        # это быстрее, чем RAND() в MySQL
        ids = cache.get('all_story_ids')
        if not ids:
            ids = tuple(self.model.objects.published.order_by('date').values_list('id', flat=True))
            cache.set('all_story_ids', ids, 300)
        if len(ids) > count:
            ids = random.sample(ids, count)
        stories = self.model.objects.filter(id__in=ids).prefetch_for_list
        return stories


class ChapterBL(BaseBL):
    def add_chapters_to_search(self, chapters):
        if settings.SPHINX_DISABLED:
            return
        chapters = [{
            'id': chapter.id,
            'title': chapter.title,
            'notes': chapter.notes,
            'text': chapter.text,
            'story_id': chapter.story.id,
            'published': chapter.story.published
        } for chapter in chapters]

        with sphinx:
            sphinx.add('chapters', chapters)

    def delete_chapters_from_search(self, chapter_ids):
        if settings.SPHINX_DISABLED:
            return
        with sphinx:
            sphinx.delete('chapters', story_id__in=chapter_ids)

    def search_add(self):
        chapter = self.model
        self.add_chapters_to_search((chapter,))
        chapter.story.bl.search_update(('words',))

    def search_update(self):
        self.search_add()

    def search_delete(self):
        chapter = self.model
        self.delete_chapters_from_search((chapter.id,))
        chapter.story.bl.search_update(('words',))

    def search(self, query, limit, only_published=True):
        if settings.SPHINX_DISABLED:
            return {}, []
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
                **sphinx_filters
            )

            ids = [x['id'] for x in raw_result['matches']]
            dresult = {x.id: x for x in self.model.objects.prefetch_related('story', 'story__authors').filter(id__in=ids)}
            result = []
            for i in ids:
                if i not in dresult:
                    continue
                excerpt = sphinx.call_snippets('chapters', dresult[i].text, query, **settings.SPHINX_CONFIG['excerpts_opts'])
                result.append((dresult[i], excerpt[0] if excerpt else ''))

        return raw_result, result
