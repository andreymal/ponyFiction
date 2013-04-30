# -*- coding: utf-8 -*-
from django.db.models import CommaSeparatedIntegerField, SubfieldBase
from ponyFiction.utils.misc import unicode_to_int_list

class SeparatedValuesField(CommaSeparatedIntegerField):
    __metaclass__ = SubfieldBase
    token = ','
    
    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return unicode_to_int_list(value)
        return unicode_to_int_list(value.split(self.token))

    def get_db_prep_value(self, value, *args, **kwargs):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([unicode(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
