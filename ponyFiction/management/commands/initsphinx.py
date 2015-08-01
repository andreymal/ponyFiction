#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import Prefetch
from django.core.management.base import BaseCommand

from ponyFiction.sphinx import sphinx
from ponyFiction.models import Story, Chapter, Author


class Command(BaseCommand):
    help = 'Load all stories and chapters into sphinx rt index'

    def handle(self, *args, **options):
        ok = 0
        pk = 0
        stories = None
        count = Story.objects.count()
        while True:
            stories = tuple(Story.objects.all().filter(pk__gt=pk).prefetch_related(
                Prefetch('authors', queryset=Author.objects.all().only('id', 'username')),
                'characters',
                'categories',
                'classifications',
                'comment_set'
            )[:500])
            if not stories:
                break

            Story.bl.add_stories_to_search(stories)
            pk = stories[-1].id
            ok += len(stories)
            self.stderr.write(' [%.1f%%] %d/%d stories\r' % (ok * 100 / count, ok, count), ending='')

        with sphinx:
            sphinx.flush('stories')

        self.stderr.write('')

        ok = 0
        pk = 0
        chapters = None
        count = Chapter.objects.count()
        while True:
            chapters = tuple(Chapter.objects.all().filter(pk__gt=pk)[:50])
            if not chapters:
                break

            Chapter.bl.add_chapters_to_search(chapters)
            pk = chapters[-1].id
            ok += len(chapters)
            self.stderr.write(' [%.1f%%] %d/%d chapters\r' % (ok * 100 / count, ok, count), ending='')

        with sphinx:
            sphinx.flush('chapters')

        self.stderr.write('')
