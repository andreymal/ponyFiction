# -*- coding: utf-8 -*-
from ponyFiction.models import Comment
from django.forms import ModelForm, Textarea 
from django.forms.fields import CharField

class CommentForm(ModelForm):
    attrs_dict = {'class': 'span4'}
    text=CharField(
        widget=Textarea(attrs=dict(attrs_dict, maxlength=8192, placeholder='Текст нового комментария')),
        max_length=8192,
        label='Добавить комментарий',
        required=False,
    )
    class Meta:
        model = Comment
        fields = ('text', )