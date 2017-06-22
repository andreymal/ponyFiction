#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core import validators
from django.db.models import CharField

from ponyFiction.utils.misc import unicode_to_int_list


class SeparatedValuesField(CharField):
    default_validators = [validators.validate_comma_separated_integer_list]

    token = ','

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return unicode_to_int_list(value)
        return unicode_to_int_list(value.split(self.token))

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def get_prep_value(self, value):
        if not value:
            return ''
        assert isinstance(value, (tuple, list)), 'SeparatedValuesField value is not list'
        return self.token.join([str(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
