#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import SelectMultiple, Widget
from django.forms.widgets import Input, TextInput
from django.forms.utils import flatatt


# Убрать при первой возможности
class NumberInput(TextInput):
    input_type = 'number'


class ButtonWidget(Widget):
    template_name = 'widgets/button.html'

    def get_context(self, name, value, attrs):
        attrs = dict(self.attrs)
        context = super().get_context(name, value, attrs)
        context['button_text'] = attrs.pop('text', '')
        context['flat_attrs'] = flatatt(attrs)
        return context


class ServiceButtonWidget(Input):
    input_type = 'submit'


class StoriesServiceInput(Widget):
    template_name = 'widgets/service_input.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['flat_attrs'] = flatatt(self.attrs)
        return context


class StoriesImgSelect(SelectMultiple):
    template_name = 'widgets/stories_img_select.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['flat_container_attrs'] = flatatt(self.attrs['container_attrs'])
        context['flat_data_attrs'] = flatatt(self.attrs['data_attrs'])
        for group, options, index in context['widget']['optgroups']:
            for option in options:
                option['img_url'] = staticfiles_storage.url('images/characters/{}.png'.format(option['value']))
        return context
