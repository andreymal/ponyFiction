# -*- coding: utf-8 -*-
from django import forms
from django.utils.encoding import force_unicode
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
import string
import ponyFiction.settings as settings

class StoriesCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None):
        # TODO: Оптимизировать (зебро)код, убрать неЛунаугодную ересь
        if value is None: value = []
        attrs = self.attrs
        label_attrs = attrs.pop('label_attrs', None)
        label_id_related_attr = attrs.pop('label_id_related_attr', False)
        output = []
        if label_attrs is not None:
            label_class = '%s' % string.join(label_attrs, ' ')
        else:
            label_class = ''        
        for (option_value, option_label) in self.choices:            
            cb = forms.widgets.CheckboxInput(attrs, check_test=lambda x: x in value)
            rendered_cb = cb.render(name, option_value)
            option_label = force_unicode(option_label)
            # TODO: Переписать
            if label_id_related_attr:
                label_id_related_class = ' '+label_id_related_attr+'%s '% option_value
            else:
                label_id_related_class = ''                
            label_class_final = ' class="%s%s"' % (label_class, label_id_related_class)
            output.append(u'<label%s>%s %s</label>' % (label_class_final, rendered_cb, option_label))
        return mark_safe(u'\n'.join(output))


class StoriesImgCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None):
        # TODO: Оптимизировать (зебро)код, убрать неЛунаугодную ересь
        if value is None: value = []
        attrs = self.attrs
        single_item_classes = attrs.pop('single_item_classes', False)
        output = []
        if single_item_classes:
            item_class = ' class="%s"' % string.join(single_item_classes, ' ')
        else:
            item_class = ''
        for (option_value, option_label) in self.choices:
            option_label = force_unicode(option_label)
            # TODO: убрать хардкод при переходе на систему аватарок
            img_url = settings.STATIC_URL+'i/characters/%s.png' % option_value
            item_image = '<img src="%s" alt="%s" title="%s" />' % (img_url, option_label, option_label)     
            cb = forms.widgets.CheckboxInput(attrs, check_test=lambda x: x in value)
            rendered_cb = cb.render(name, option_value)            
            output.append(u'<span%s>%s%s</span>' % (item_class, item_image, rendered_cb))
        return mark_safe(u'\n'.join(output))
    
class ButtonWidget(forms.Widget):
    def render(self, name=None, value=None, attrs=None):
        attrs = self.attrs
        text = attrs.pop('text', '')
        return mark_safe(u'<button%s>%s</button>' % (flatatt(attrs), force_unicode(text)))
    
class ServiceButtonWidget(forms.widgets.Input):
    input_type = 'submit'

class StoriesServiceInput(forms.Widget):
    def render(self, name=None, value=None, attrs=None):
        return mark_safe(u'<input%s />' % flatatt(self.attrs))

class StoriesButtons(forms.CheckboxSelectMultiple):
    # TODO: Проверить на баги
    def render(self, name, value, attrs=None):
        # TODO: Оптимизировать (зебро)код, убрать неЛунаугодную ересь
        if value is None: value = []
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
            cb = forms.widgets.CheckboxInput(data_attrs, check_test=lambda x: x in value)
            rendered_cb = cb.render(name, option_value)
            data_container.append(rendered_cb)
        # TODO: Упростить, убрав излишний код 
        btn = '<div%s>%s</div>' % (flatatt(btn_container_attrs), string.join(btn_container))
        data = '<div%s>%s</div>' % (flatatt(data_container_attrs), string.join(data_container))
        output.append(btn)
        output.append(data)
        return mark_safe(u'\n'.join(output))

   
class StoriesRadioFieldRenderer(forms.widgets.RadioFieldRenderer):
    def render(self):
        attrs = self.attrs
        name = self.name
        value = self.value
        # TODO: Переписать!
        if (value == 'True'):
            value = 1
        elif (value == 'False'):
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
        # TODO: Упростить, убрав излишний код 
        btn = '<div%s>%s</div>' % (flatatt(btn_container_attrs), string.join(btn_container))
        data = '<div%s>%s</div>' % (flatatt(data_container_attrs), string.join(data_container))
        output.append(btn)
        output.append(data)
        return mark_safe(u'\n'.join(output))

class StoriesRadioButtons(forms.widgets.RadioSelect):
    renderer = StoriesRadioFieldRenderer