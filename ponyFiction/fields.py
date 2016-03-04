#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import CommaSeparatedIntegerField, SubfieldBase

from ponyFiction.utils.misc import unicode_to_int_list


class SeparatedValuesField(CommaSeparatedIntegerField, metaclass=SubfieldBase):
    token = ','

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return unicode_to_int_list(value)
        return unicode_to_int_list(value.split(self.token))

    def get_db_prep_value(self, value, *args, **kwargs):
        if not value:
            return
        assert isinstance(value, (tuple, list)), 'SeparatedValuesField value is not list'
        return self.token.join([str(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
