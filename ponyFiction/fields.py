# -*- coding: utf-8 -*-
from django.forms.models import ModelChoiceIterator
from django.forms import ModelChoiceField, ModelMultipleChoiceField, CharField
from itertools import groupby
import bleach

class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    (group, [self.choice(ch) for ch in choices])
                        for group,choices in groupby(self.queryset.all(),
                            key=lambda row: getattr(row, self.field.group_by_field))
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
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
    
class SanitizedCharField(CharField):
    """
    A subclass of CharField that escapes (or strip) HTML tags and attributes.
    """    
    def __init__(self, allowed_tags=[], allowed_attributes=[], 
            allowed_styles=[], strip=False, *args, **kwargs):
        self._allowed_tags = allowed_tags
        self._allowed_attributes = allowed_attributes
        self._allowed_styles = allowed_styles
        self._strip = strip
        super(SanitizedCharField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(SanitizedCharField, self).clean(value)
        return bleach.clean(value, tags=self._allowed_tags,
            attributes=self._allowed_attributes, 
            styles=self._allowed_styles, strip=self._strip)