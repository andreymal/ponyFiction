# -*- coding: utf-8 -*-
from django.forms import CharField, Field, ModelForm, TextInput, Textarea
from sanitizer.forms import SanitizedCharField
from ponyFiction.stories.models import Chapter
from ponyFiction.stories.widgets import ServiceButtonWidget
from ponyFiction import settings as settings

class ChapterForm(ModelForm):
    """
    Форма добавления новой главы к рассказу
    TODO: Добавить "заметки к главе" 
    """
    textarea_dict = {'class': 'input-xlarge chapter-textarea'}
    attrs_dict = {'class': 'input-xlarge'}
    # Название
    title = CharField(
        required=True,
        widget=TextInput(attrs=dict(attrs_dict, maxlength=512, placeholder= 'Заголовок новой главы')),
        label='Название',
        max_length=512,
        error_messages={'required': 'Пожалуйста, назовите новую главу вашего рассказа'},
    )
    text=SanitizedCharField(
        widget=Textarea(attrs=dict(textarea_dict, placeholder='Текст новой главы')),
        label='Текст главы',
        allowed_tags=settings.SANITIZER_ALLOWED_TAGS,
        allowed_attributes=settings.SANITIZER_ALLOWED_ATTRIBUTES,
        required=False,
    )
    # Заметки к главе
    notes=SanitizedCharField(
        required=False,
        widget=Textarea(attrs=dict(attrs_dict, rows=4, cols=10, maxlength=4096, placeholder='Заметки к главе')),
        max_length=4096,
        label='Заметки',
        help_text='Заметки автора к главе',
    )
    # Кнопка "Отправить"
    button_submit = Field(
        required=False,
        widget=ServiceButtonWidget(attrs={'class': 'btn btn-primary'}),
    )
    # Кнопка "Удалить"
    button_delete = Field(
        required=False,
        widget=ServiceButtonWidget(attrs={'class': 'btn btn-danger'}),
        initial='Удалить главу',
    )
    # Метакласс
    class Meta:
        model = Chapter
        fields = ('title', 'text')