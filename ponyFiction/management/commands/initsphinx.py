#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import Prefetch
from django.core.management.base import BaseCommand

from ponyFiction import models
from ponyFiction.sphinx import sphinx, add_stories, add_chapters


class Command(BaseCommand):
    help = 'Load all stories and chapters into sphinx rt index'

    def handle(self, *args, **options):
        ok = 0
        pk = 0
        stories = None
        count = models.Story.objects.count()
        while True:
            stories = tuple(models.Story.objects.all().filter(pk__gt=pk).prefetch_related(
                Prefetch('authors', queryset=models.Author.objects.all().only('id', 'username')),
                'characters',
                'categories',
                'classifications',
                'comment_set'
            )[:500])
            if not stories:
                break

            with sphinx:
                add_stories(stories)
            pk = stories[-1].id
            ok += len(stories)
            self.stderr.write(' [%.1f%%] %d/%d stories\r' % (ok * 100 / count, ok, count), ending='')

        with sphinx:
            sphinx.flush('stories')

        self.stderr.write('')

        ok = 0
        pk = 0
        chapters = None
        count = models.Chapter.objects.count()
        while True:
            chapters = tuple(models.Chapter.objects.all().filter(pk__gt=pk)[:50])
            if not chapters:
                break

            with sphinx:
                add_chapters(chapters)
            pk = chapters[-1].id
            ok += len(chapters)
            self.stderr.write(' [%.1f%%] %d/%d chapters\r' % (ok * 100 / count, ok, count), ending='')

        with sphinx:
            sphinx.flush('chapters')

        self.stderr.write('')
