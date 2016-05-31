# -*- coding: utf-8 -*-
from django.conf import settings
from ponyFiction.models import Comment
from django.forms import ModelForm, Textarea, ValidationError
from django.forms.fields import CharField
from django.template.defaultfilters import striptags


class CommentForm(ModelForm):
    attrs_dict = {'class': 'col-md-4 form-control'}
    text = CharField(
        widget=Textarea(attrs=dict(attrs_dict, maxlength=8192, placeholder='Текст нового комментария')),
        max_length=8192,
        label='Добавить комментарий',
        required=False,
    )

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(striptags(text)) < settings.COMMENT_MIN_LENGTH:
            raise ValidationError('Сообщение слишком короткое!')
        return text

    class Meta:
        model = Comment
        fields = ('text', )
