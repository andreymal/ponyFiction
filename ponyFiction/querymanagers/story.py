from django.db import models
from django.db.models import Prefetch


class StoryQuerySet(models.query.QuerySet):
    @property
    def prefetch_for_list(self):
        from ponyFiction.models import Author
        return self.prefetch_related(
            Prefetch('authors', queryset=Author.objects.all().only('username')),
            'characters',
            'categories'
        )

    @property
    def published(self):
        return self.filter(draft=False, approved=True)

    @property
    def submitted(self):
        return self.filter(draft=False, approved=False)

    @property
    def good(self):
        return self

    @property
    def last_week(self):
        return self.filter(date__gte=self.last)

    def accessible(self, user):
        default_queryset = self.filter(draft=False, approved=True)
        if not user.is_authenticated():
            return default_queryset
        if user.is_staff:
            return self
        else:
            return default_queryset.exclude(categories__in=user.excluded_categories)

        # from datetime import date, timedelta
        # last = date.today() - timedelta(weeks=1)
        # All NOT drafts AND (already approved OR (submitted at last 1 week ago AND NOT approved yet) ) stories
        # default_queryset = self.filter(Q(date__lte=last, approved=False)|Q(approved=True), draft=False)


class StoryManager(models.Manager):
    def get_queryset(self):
        return StoryQuerySet(self.model, using=self._db)

    def __getattr__(self, attr):
        if attr.startswith('_') or attr == 'model':
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__, attr))
        try:
            return getattr(self.__class__, attr)
        except AttributeError:
            return getattr(self.get_queryset(), attr)