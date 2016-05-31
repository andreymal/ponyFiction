# -*- coding: utf-8 -*-
from django.forms import CharField, Field, ModelForm, TextInput, Textarea
from ponyFiction.models import Chapter
from ponyFiction.widgets import ServiceButtonWidget


class ChapterForm(ModelForm):
    """ Форма добавления новой главы к рассказу """
    textarea_dict = {'class': 'form-control chapter-textarea'}
    attrs_dict = {'class': 'form-control'}

    # Название
    title = CharField(
        required=True,
        widget=TextInput(attrs=dict(attrs_dict, maxlength=512, placeholder='Заголовок новой главы')),
        label='Название',
        max_length=512,
        error_messages={'required': 'Пожалуйста, назовите новую главу вашего рассказа'},
    )

    # Текст главы
    text = CharField(
        widget=Textarea(attrs=dict(textarea_dict, placeholder='Текст новой главы')),
        label='Текст главы',
        required=False,
        max_length=300000,
    )

    # Заметки к главе
    notes = CharField(
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

    # Метакласс
    class Meta:
        model = Chapter
        fields = ('title', 'text', 'notes')
