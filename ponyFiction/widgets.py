#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import SelectMultiple, CheckboxSelectMultiple, Widget
from itertools import chain
from django.forms.widgets import CheckboxInput, Input, RadioFieldRenderer, RadioSelect, TextInput
try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt


# Убрать при первой возможности
class NumberInput(TextInput):
    input_type = 'number'


class ButtonWidget(Widget):
    def render(self, name=None, value=None, attrs=None):
        attrs = self.attrs
        text = attrs.pop('text', '')
        return mark_safe('<button%s>%s</button>' % (flatatt(attrs), force_unicode(text)))


class ServiceButtonWidget(Input):
    input_type = 'submit'


class StoriesServiceInput(Widget):
    def render(self, name=None, value=None, attrs=None):
        return mark_safe('<input%s />' % flatatt(self.attrs))


class StoriesCheckboxSelectMultiple(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        value = [int(x) for x in value]
        attrs = self.attrs
        label_attrs = attrs.pop('label_attrs', None)
        label_id_related_attr = attrs.pop('label_id_related_attr', False)
        output = []
        if label_attrs is not None:
            label_class = '%s' % ' '.join(label_attrs)
        else:
            label_class = ''
        for (option_value, option_label) in self.choices:
            cb = CheckboxInput(attrs, check_test=lambda x: x in value)
            rendered_cb = cb.render(name, option_value)
            option_label = force_unicode(option_label)
            if label_id_related_attr:
                label_id_related_class = ' '+label_id_related_attr+'%s ' % option_value
            else:
                label_id_related_class = ''
            label_class_final = ' class="%s%s"' % (label_class, label_id_related_class)
            output.append('<label%s>%s %s</label>' % (label_class_final, rendered_cb, option_label))
        return mark_safe('\n'.join(output))


class StoriesImgSelect(SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        value = [int(x) for x in value]
        output = []
        attrs = self.attrs
        group_container_class = attrs['group_container_class']
        for group, option_sublist in chain(self.choices, choices):
            output.append('<span class="%s%s" title="%s">' % (group_container_class, group.id, group.name))
            for option in option_sublist:
                # *option == (int, string)
                output.append(self.render_option(attrs, name, value, *option))
            output.append('</span>')
        return mark_safe('\n'.join(output))

    def render_option(self, attrs, name, selected_choices, option_value, option_label):
        container_attrs = attrs['container_attrs']
        data_attrs = attrs['data_attrs']
        img_url = staticfiles_storage.url('images/characters/{}.png'.format(option_value))
        img_class = 'ui-selected' if option_value in selected_choices else ''
        item_image = '<img class="%s" src="%s" alt="%s" title="%s" />' % (img_class, img_url, option_label, option_label)
        cb = CheckboxInput(data_attrs, check_test=lambda x: x in selected_choices)
        rendered_cb = cb.render(name, option_value)
        return mark_safe('<span%s>%s%s</span>' % (flatatt(container_attrs), rendered_cb, item_image))


class StoriesButtons(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        attrs = self.attrs
        btn_attrs = attrs.pop('btn_attrs', {})
        data_attrs = attrs.pop('data_attrs', {})
        btn_container_attrs = attrs.pop('btn_container_attrs', {})
        data_container_attrs = attrs.pop('data_container_attrs', {})
        btn_container = []
        data_container = []
        output = []
        for (option_value, option_label) in self.choices:
            option_label = force_unicode(option_label)
            btn = ButtonWidget(attrs=dict(btn_attrs, text=option_label, value=option_value))
            rendered_btn = btn.render(attrs=btn_attrs)
            btn_container.append(rendered_btn)
            cb = CheckboxInput(data_attrs, check_test=lambda x: str(x) in value)
            rendered_cb = cb.render(name, option_value)
            data_container.append(rendered_cb)
        btn = '<div%s>%s</div>' % (flatatt(btn_container_attrs), ' '.join(btn_container))
        data = '<div%s>%s</div>' % (flatatt(data_container_attrs), ' '.join(data_container))
        output.append(btn)
        output.append(data)
        return mark_safe('\n'.join(output))


class StoriesRadioFieldRenderer(RadioFieldRenderer):
    def render(self):
        attrs = self.attrs
        name = self.name
        value = self.value
        if value == 'True':
            value = 1
        elif value == 'False':
            value = 0
        else:
            value = int(value) if value else False
        btn_attrs = attrs.pop('btn_attrs', {})
        data_attrs = attrs.pop('data_attrs', {})
        btn_container_attrs = attrs.pop('btn_container_attrs', {})
        data_container_attrs = attrs.pop('data_container_attrs', {})
        btn_container = []
        data_container = []
        output = []
        for (option_value, option_label) in self.choices:
            option_label = force_unicode(option_label)
            btn = ButtonWidget(attrs=dict(btn_attrs, text=option_label, value=option_value))
            rendered_btn = btn.render(attrs=btn_attrs)
            btn_container.append(rendered_btn)
            if option_value == value:
                rb = StoriesServiceInput(attrs=dict(data_attrs, type='radio', name=name, value=option_value, checked='checked'))
            else:
                rb = StoriesServiceInput(attrs=dict(data_attrs, type='radio', name=name, value=option_value))
            rendered_rb = rb.render(name, value)
            data_container.append(rendered_rb)
        btn = '<div%s>%s</div>' % (flatatt(btn_container_attrs), ' '.join(btn_container))
        data = '<div%s>%s</div>' % (flatatt(data_container_attrs), ' '.join(data_container))
        output.append(btn)
        output.append(data)
        return mark_safe('\n'.join(output))


class StoriesRadioButtons(RadioSelect):
    renderer = StoriesRadioFieldRenderer
