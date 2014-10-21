from django.db.models.query import QuerySet


QuerySet.cache = lambda self, *a, **kw: self