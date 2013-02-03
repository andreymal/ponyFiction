# -*- coding: utf-8 -*-
from django.forms import CharField, ChoiceField, Field, ModelForm, ModelChoiceField, ModelMultipleChoiceField, TextInput, Textarea
from ponyFiction.stories.fields import GroupedModelChoiceField
from ponyFiction.stories.models import Character, Category, Classifier, Rating, Size, Story
from ponyFiction.stories.widgets import ServiceButtonWidget, StoriesImgSelect, StoriesCheckboxSelectMultiple, StoriesRadioButtons
from sanitizer.forms import SanitizedCharField

class StoryForm(ModelForm):
    attrs_dict = {'class': 'input-xlarge'}
    img_attrs = {
           'group_container_class': 'characters-group group-',
           'data_attrs': {'class': 'hidden'},
           'container_attrs': {'class': 'character-item'}
    }  
    radio_attrs={
           'btn_attrs': {'type': 'button', 'class': 'btn'},
           'data_attrs': {'class': 'hidden'},
           'btn_container_attrs': {'class': 'btn-group buttons-visible', 'data-toggle': 'buttons-radio'},
           'data_container_attrs': {'class': 'buttons-data'},
           }
    checkbox_attrs={
           'btn_attrs': {'type': 'button', 'class': 'btn'},
           'data_attrs': {'class': 'hidden'},
           'btn_container_attrs': {'class': 'btn-group buttons-visible', 'data-toggle': 'buttons-checkbox'},
           'data_container_attrs': {'class': 'buttons-data'},
           }
    # Персонажи
    characters = GroupedModelChoiceField(
        required=False,
        queryset=Character.objects.all(),
        group_by_field='group',
        widget=StoriesImgSelect(attrs=img_attrs),
        label='Персонажи',
        help_text='Следует выбрать персонажей, находящихся в гуще событий, а не всех пони, упомянутых в произведении.',
    )
    # Жанры
    categories = ModelMultipleChoiceField(
        required=True,
        queryset=Category.objects.all(),
        widget=StoriesCheckboxSelectMultiple(
        attrs={'label_attrs': ['checkbox', 'inline', 'gen'],'label_id_related_attr': 'gen-'}),
        label='Жанры',
        help_text='Выберите жанр вашего рассказа',
        error_messages={'required': 'Жанры - обязательное поле'}
    )
    # События
    classifications = ModelMultipleChoiceField(
        required=False,
        queryset=Classifier.objects.all(),
        widget=StoriesCheckboxSelectMultiple(attrs={'label_attrs': ['checkbox', 'inline']}),
        label='События',
        help_text='Ключевые события рассказа',
    )
    # Закончен/не закончен
    finished = ChoiceField(
        required=True,
        choices=[(0, 'Не закончен'),(1, 'Закончен')],
        widget=StoriesRadioButtons(attrs=radio_attrs),
        label='Статус',
        help_text='Завершен ли рассказ',
        error_messages={'required': 'Нужно обязательно указать статус рассказа!'},
    )
    # Заморожен/активен
    freezed = ChoiceField(
        required=True,
        choices=[(0, 'Активен'),(1, 'Заморожен')],
        widget=StoriesRadioButtons(attrs=radio_attrs),
        label='Состояние',
        help_text='Активность рассказа (пишется ли он сейчас)',
        error_messages={'required': 'Нужно обязательно указать состояние рассказа!'},
    )
    # Оригинал/перевод
    original = ChoiceField(
        required=True,
        choices=[(1, 'Оригинал'), (0, 'Перевод')],
        widget=StoriesRadioButtons(attrs=radio_attrs),
        label='Происхождение',
        error_messages={'required': 'Нужно обязательно указать происхождение рассказа!'},
    )
    # Рейтинг
    rating = ModelChoiceField(
        required=True,
        empty_label=None,
        queryset=Rating.objects.order_by('-id'),
        widget=StoriesRadioButtons(attrs=radio_attrs),
        label='Рейтинг',
        error_messages={'required': 'Нужно обязательно указать рейтинг рассказа!'},
    )
    # Краткое описание рассказа
    summary=SanitizedCharField(
        required=True,
        widget=Textarea(attrs=dict(attrs_dict, maxlength=4096, placeholder='Обязательное краткое описание рассказа')),
        max_length=4096,
        label='Краткое описание рассказа',
        error_messages={'required': 'Опишите вкратце содержание рассказа - это обязательное поле'},
    )
    # Заметки к рассказу
    notes=SanitizedCharField(
        required=False,
        widget=Textarea(attrs=dict(attrs_dict, maxlength=4096, placeholder='Заметки к рассказу')),
        max_length=4096,
        label='Заметки',
    )
    # Размер
    size = ModelChoiceField(
        required=True,
        empty_label=None,
        queryset=Size.objects.all(),
        widget=StoriesRadioButtons(attrs=radio_attrs),
        label='Размер',
        error_messages={'required': 'Нужно обязательно указать размер рассказа!'},
    )
    # Название
    title = CharField(
        required=True,
        widget=TextInput(attrs=dict(attrs_dict, maxlength=512, placeholder= 'Заголовок нового рассказа')),
        label='Название',
        max_length=512,
        error_messages={'required': 'Пожалуйста, назовите ваш рассказ'},
    )
    # Кнопка "Сохранить"
    button_submit = Field(
        required=False,
        widget=ServiceButtonWidget(attrs={'class': 'btn btn-primary'}),
        initial = 'Сохранить'
    )
    # Кнопка "Удалить"
    button_delete = Field(
        required=False,
        widget=ServiceButtonWidget(attrs={'class': 'btn btn-danger'}),
        initial='Удалить рассказ',
    )
    # Метакласс
    class Meta:
        model = Story
        fields = ('characters', 'categories', 'classifications', 'finished',
                  'freezed', 'original', 'rating', 'summary', 'notes', 'size', 'title')
