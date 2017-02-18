import types

from django.db.models import Manager
from django.db.models import QuerySet


def factory(queryset_class=QuerySet):
    def get_queryset(self):
        return queryset_class(self.model, using=self._db)

    def __getattr__(self, attr):
        if attr.startswith('_') or attr == 'model':
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__, attr))
        try:
            return getattr(self.__class__, attr)
        except AttributeError:
            return getattr(self.get_queryset(), attr)

    cls_dict = dict(
        __getattr__=__getattr__,
        get_queryset=get_queryset
    )

    cls = types.new_class(
        "{0.__name__}ProxyManager".format(queryset_class),
        (Manager,),
        {},
        lambda ns: ns.update(cls_dict)
    )
    cls.__module__ = __name__
    return cls()
