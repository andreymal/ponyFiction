# -*- coding: utf-8 -*-
from django import forms
from registration.forms import RegistrationForm
from ponyFiction.stories.apis.recaptcha import fields as captcha_fields
from ponyFiction.stories.models import Author, Comment, Category, Classifier, Character, Rating, Size, Story
from ponyFiction.widgets import StoriesCheckboxSelectMultiple, StoriesImgCheckboxSelectMultiple, StoriesButtons, ButtonWidget, ServiceButtonWidget, StoriesServiceInput, StoriesRadioButtons
from sanitizer.forms import SanitizedCharField
import ponyFiction.settings as settings
#import pydevd
class AuthorRegistrationForm(RegistrationForm):
    attrs_dict = {'class': 'required input-xlarge'}
    username = forms.RegexField(
        regex=ur'^[0-9a-zA-Z\u0430-\u044f\u0410-\u042f\u0451\u0401_@+-.. ]+$',
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=32)),
        max_length=32,
        label='Логин',
        help_text='Только русские/латинские буквы, цифры, пробел, точка и символы _ @ + -',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в логине - он может содержать только русские/латинские буквы, цифры, пробел, точку и символы _ @ + -'}
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)),
        max_length=75,
        label='Электропочта',
        help_text='Адрес электронной почты для активации аккаунта',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в адресе e-mail: похоже, он неправильный'}
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label="Пароль",
        help_text='Выбирайте сложный пароль',
        )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label="Пароль (опять)",
        help_text='Повторите пароль, чтобы не забыть',
        )
    recaptcha = captcha_fields.ReCaptchaField(
        label="Капча",
        help_text='Введите два слова выше. Если трудно разобрать, обновите.',
        error_messages={'captcha_invalid': 'Это какая-то неправильная капча. Пожалуйста, введите снова.'}
        )

class AuthorEditProfileForm(forms.ModelForm):
    attrs_dict = {'class': 'input-xlarge'}
    bio=SanitizedCharField(
        widget=forms.Textarea(attrs=dict(attrs_dict, maxlength=2048, placeholder='Небольшое описание, отображается в профиле')),
        max_length=2048,
        label='Пару слов о себе',
        required=False,
    )
    jabber = forms.EmailField(
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75, placeholder='Адрес jabber-аккаунта')),
        max_length=75,
        label='Jabber ID (XMPP)',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в адресе jabber: похоже, он неправильный'},
        required=False,
    )
    
    skype = forms.RegexField(
        regex=ur'^[a-zA-Z0-9-_]+$',
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=32, placeholder='Логин skype')),
        max_length=32,
        label='Skype ID',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в логине skype: похоже, он неправильный'},
        required=False
    )
    tabun = forms.RegexField(
        regex=ur'^[a-zA-Z0-9-_]+$',
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=32)),
        max_length=32,
        label='Логин на Табуне',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в имени пользователя: похоже, оно неправильно'},
       required=False
    )
    forum = forms.URLField(
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=32, placeholder='URL вашего профиля')),
        max_length=32,
        label='Адрес профиля на Форуме',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку адресе профиля: похоже, он неправильный.'},
        required=False
    )
    vk = forms.RegexField(
        regex=ur'^[a-zA-Z0-9-_]+$',
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=32)),
        max_length=32,
        label='Логин ВКонтакте',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в логине VK: похоже, он неправильный'},
        required=False
    )
    class Meta:
        model = Author
        fields = ('bio', 'jabber', 'skype', 'tabun', 'forum', 'vk')

class AuthorEditEmailForm(forms.Form):
    attrs_dict = {'class': 'input-xlarge'}
    
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75, placeholder='Адрес электронной почты')),
        max_length=75,
        label='Электропочта',
        error_messages={'invalid': 'Пожалуйста, исправьте ошибку в адресе e-mail: похоже, он неправильный'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(attrs_dict, placeholder='****************'), render_value=False),
        label="Пароль",
        help_text='Для безопасной смены почты введите пароль',
    )
    
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(AuthorEditEmailForm, self).__init__(*args, **kwargs)
        if self.author:
            self.fields['email'].initial = self.author.email
    
    def clean(self):
        cleaned_data = super(AuthorEditEmailForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            if not self.author.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return cleaned_data
    
    def save(self):
        author = self.author
        email = self.cleaned_data['email']
        author.email = email
        author.save()
        
class AuthorEditPasswordForm(forms.Form):
    attrs_dict = {'class': 'input-xlarge'}
    
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(attrs_dict, placeholder='****************'), render_value=False),
        label="Старый пароль",
        help_text='Для безопасной смены пароля введите старый пароль',
    )
    new_password_1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(attrs_dict, placeholder='****************'), render_value=False),
        label="Новый пароль",
        help_text='Выбирайте сложный пароль',
    )
    new_password_2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(attrs_dict, placeholder='****************'), render_value=False),
        label="Новый пароль (опять)",
        help_text='Повторите новый пароль, чтобы не забыть',
        )
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(AuthorEditPasswordForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(AuthorEditPasswordForm, self).clean()
        old_password = cleaned_data.get('old_password')
        new_password_1 = cleaned_data.get('new_password_1')
        new_password_2 = cleaned_data.get('new_password_2')
        
        if old_password and new_password_1 and new_password_2:
            if self.author.check_password(old_password):
                if new_password_1 != new_password_2:
                    raise forms.ValidationError('Пароли не совпадают')
            else:
                raise forms.ValidationError('Пароль неверный')
        else:
            raise forms.ValidationError('Введены не все данные')
        
        return cleaned_data
    
    def save(self):
        author = self.author
        password = self.cleaned_data['new_password_1']
        author.set_password(password)
        author.save()

class StoryAddComment(forms.ModelForm):
    attrs_dict = {'class': 'span4'}
    text=SanitizedCharField(
        widget=forms.Textarea(attrs=dict(attrs_dict, maxlength=8192, placeholder='Текст нового комментария')),
        max_length=8192,
        label='Добавить комментарий',
        allowed_tags=settings.SANITIZER_ALLOWED_TAGS,
        allowed_attributes=settings.SANITIZER_ALLOWED_ATTRIBUTES,
        required=False,
    )
    class Meta:
        model = Comment
        fields = ('text', )

class SearchForm(forms.Form):
    checkbox_attrs={
           'btn_attrs': {'type': 'button', 'class': 'btn'},
           'data_attrs': {'class': 'hidden'},
           'btn_container_attrs': {'class': 'btn-group buttons-visible', 'data-toggle': 'buttons-checkbox'},
           'data_container_attrs': {'class': 'buttons-data'},
           }
    # Строка поиска
    search_query = SanitizedCharField(
        required=False,
        widget=forms.TextInput(
            attrs={
               'size': 32,
               'placeholder': 'Пинки-поиск',
               'id': 'appendedInputButtons',
               'class': 'span3',
               'maxlength': 128,
            }
        ),
        max_length=128,
    )
    # Жанры
    categories_select = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=StoriesCheckboxSelectMultiple(
            attrs={
                   'label_attrs': ['checkbox', 'inline', 'gen'],
                   'label_id_related_attr': 'gen-',
                   },
        ),
    )
    # Персонажи
    characters_select = forms.ModelMultipleChoiceField(
        queryset=Character.objects.all(),
        required=False,
        widget=StoriesImgCheckboxSelectMultiple(attrs={'class': 'hidden', 'single_item_classes': ['character-item',]}),
    )
    # Оригинал/перевод
    originals_select = forms.MultipleChoiceField(
        choices=[(0, 'Перевод'),(1, 'Оригинал')],
        required=False,
        widget=StoriesButtons(attrs=checkbox_attrs),
    )
    # Статус истории
    finished_select = forms.MultipleChoiceField(
        choices=[(0, 'Не завершен'),(1, 'Завершен')],
        required=False,
        widget=StoriesButtons(attrs=checkbox_attrs),
    )
    # Активность истории
    freezed_select = forms.MultipleChoiceField(
        choices=[(0, 'Активен'),(1, 'Заморожен')],
        required=False,
        widget=StoriesButtons(attrs=checkbox_attrs),
    )
    # Размеры
    sizes_select = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
        required=False,
        widget=StoriesButtons(attrs=checkbox_attrs),
    )
    # Рейтинги
    ratings_select = forms.ModelMultipleChoiceField(
        queryset=Rating.objects.all(),
        required=False,
        widget=StoriesButtons(attrs=checkbox_attrs),
    )
    # События
    classifications_select = forms.ModelMultipleChoiceField(
        queryset=Classifier.objects.all(),
        required=False,
        widget=StoriesCheckboxSelectMultiple(attrs={'label_attrs': ['checkbox', 'inline']}),
    )
    # Кнопка "Развернуть"
    button_advanced = forms.Field(
        required=False,
        widget=ButtonWidget(
            attrs={
                   'type': 'button',
                   'class': 'btn btn-collapse btn-small',
                   'data-toggle': 'collapse',
                   'data-target': '#more-info',
                   'text': 'Еще более тонкий поиск'
                   }
        ),
    )
    
    button_submit = forms.Field(
        required=False,
        widget=ServiceButtonWidget(attrs={'class': 'btn btn-primary'}),
        initial='Искать!',
    )

    button_reset = forms.Field(
        required=False,
        widget=StoriesServiceInput(
            attrs={
                   'type': 'reset',
                   'class': 'btn',
                   'id': 'reset_search',
                   'value': 'Очистить',
                   }
        ),
    )

class StoryAdd(forms.ModelForm):
    attrs_dict = {'class': 'input-xlarge'}   
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
    characters = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Character.objects.all(),
        widget=StoriesImgCheckboxSelectMultiple(attrs={'class': 'hidden','single_item_classes': ['character-item',]}),
        label='Персонажи',
        help_text='Следует выбрать персонажей, находящихся в гуще событий, а не всех пони, упомянутых в произведении.',
    )
    # Жанры
    categories = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Category.objects.all(),
        widget=StoriesCheckboxSelectMultiple(
        attrs={'label_attrs': ['checkbox', 'inline', 'gen'],'label_id_related_attr': 'gen-'}),
        label='Жанры',
        help_text='Выберите жанр вашего рассказа',
        error_messages={'required': 'Жанры - обязательное поле'}
    )
    # События
    classifications = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Classifier.objects.all(),
        widget=StoriesCheckboxSelectMultiple(attrs={'label_attrs': ['checkbox', 'inline']}),
        label='События',
        help_text='Ключевые события рассказа',
    )
    # Заморожен/активен
    freezed = forms.ChoiceField(
        required=True,
        choices=[(0, 'Активен'),(1, 'Заморожен')],
        widget=StoriesRadioButtons(attrs=radio_attrs),
        label='Статус',
        help_text='Активность рассказа (пишется ли он сейчас)',
        error_messages={'required': 'Нужно обязательно указать статус рассказа!'},
    )
    # Заметки к рассказу
    notes=SanitizedCharField(
        required=False,
        widget=forms.Textarea(attrs=dict(attrs_dict, rows=4, cols=10, maxlength=4096, placeholder='Заметки к рассказу')),
        max_length=4096,
        label='Заметки',
        help_text='Заметки автора к рассказу',
    )
    # Оригинал/перевод
    original = forms.ChoiceField(
        required=True,
        choices=[(1, 'Оригинал'), (0, 'Перевод')],
        widget=StoriesRadioButtons(attrs=radio_attrs),
        label='Происхождение',
        error_messages={'required': 'Нужно обязательно указать происхождение рассказа!'},
    )
    # Рейтинг
    rating = forms.ModelChoiceField(
        required=True,
        empty_label=None,
        queryset=Rating.objects.all(),
        widget=StoriesRadioButtons(attrs=radio_attrs),
        label='Рейтинг',
        help_text='О рейтингах',
        error_messages={'required': 'Нужно обязательно указать рейтинг рассказа!'},
    )
    # Краткое описание рассказа
    summary=SanitizedCharField(
        required=True,
        widget=forms.Textarea(attrs=dict(attrs_dict, rows=4, cols=10, maxlength=4096, placeholder='Обязательное краткое описание рассказа')),
        max_length=4096,
        label='Краткое описание рассказа',
        error_messages={'required': 'Опишите вкратце содержание рассказа - это обязательное поле'},
    )
    # Размер
    size = forms.ModelChoiceField(
        required=True,
        empty_label=None,
        queryset=Size.objects.all(),
        widget=StoriesRadioButtons(attrs=radio_attrs),
        label='Размер',
        help_text='О размерах',
        error_messages={'required': 'Нужно обязательно указать размер рассказа!'},
    )
    # Название
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=512, placeholder= 'Заголовок нового рассказа')),
        label='Название',
        max_length=512,
        error_messages={'required': 'Пожалуйста, назовите ваш рассказ'},
    )
    # Кнопка "Отправить"
    button_submit = forms.Field(
        required=False,
        widget=ServiceButtonWidget(attrs={'class': 'btn btn-primary'}),
    )
    # Кнопка "Удалить"
    button_delete = forms.Field(
        required=False,
        widget=ServiceButtonWidget(attrs={'class': 'btn btn-danger'}),
        initial='Удалить рассказ',
    )
    # Метакласс
    class Meta:
        model = Story
        fields = ('characters', 'categories','classifications', 'freezed', 'original', 'rating', 'summary', 'size', 'title')