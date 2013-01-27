# -*- coding: utf-8 -*-
from ponyFiction.stories.models import Comment
from ponyFiction import settings as settings
from django.forms import ModelForm, Textarea 
from sanitizer.forms import SanitizedCharField


class CommentForm(ModelForm):
    attrs_dict = {'class': 'span4'}
    text=SanitizedCharField(
        widget=Textarea(attrs=dict(attrs_dict, maxlength=8192, placeholder='Текст нового комментария')),
        max_length=8192,
        label='Добавить комментарий',
        allowed_tags=settings.SANITIZER_ALLOWED_TAGS,
        allowed_attributes=settings.SANITIZER_ALLOWED_ATTRIBUTES,
        required=False,
    )
    class Meta:
        model = Comment
        fields = ('text', )