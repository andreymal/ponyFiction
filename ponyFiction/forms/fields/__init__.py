#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms.models import ModelChoiceIterator
from django.forms import ModelChoiceField, ModelMultipleChoiceField
from itertools import groupby


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ('', self.field.empty_label)
        for group, choices in groupby(self.queryset.order_by('group'), lambda row: getattr(row, self.field.group_by_field)):
            yield (group, [self.choice(ch) for ch in choices])


class GroupedModelChoiceField(ModelMultipleChoiceField):
    def __init__(self, queryset, group_by_field, group_label=None, *args, **kwargs):
        """
        group_by_field is the name of a field on the model
        group_label is a function to return a label for each choice group
        """
        super(GroupedModelChoiceField, self).__init__(queryset, *args, **kwargs)
        self.group_by_field = group_by_field
        if group_label is None:
            self.group_label = lambda group: group
        else:
            self.group_label = group_label

    def _get_choices(self):
        """
        Exactly as per ModelChoiceField except returns new iterator class
        """
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)
    choices = property(_get_choices, ModelChoiceField._set_choices)
